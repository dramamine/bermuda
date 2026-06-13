/*
Accept Artnet data and display it, through an OctoWS2811 / Teensy / Wiz850io

Install Teensyduino and set board to "Teensy 4.1"

10/13: made this more flexible/generic and added the ability to send multiple
universes per data channel. From testing I think you can send 4 universes per
channel for a combined 32 universes of LED data.

9/12: fixed the 34=>35 conversion bug that I found at the campsite
added constellations but haven't tested or made fancy yet

from 7/23: updated the Artnet library to use NativeEthernet and NativeEthernetUdp
it "just works" after that. tried to use #define TEENSY41 to conditionally load
those specific libraries but that wasn't working for me, was still trying to load
the normal Ethernat library.
After warming up, this was getting 40 fps with 3 universes.

The MIT License (MIT)

Copyright (c) 2018-2024 Marten Silbiger
https://github.com/dramamine/lightdream-scripts

Copyright (c) 2014 Nathanaël Lécaudé
https://github.com/natcl/Artnet, http://forum.pjrc.com/threads/24688-Artnet-to-OctoWS2811

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Resources:
https://www.pjrc.com/teensy/td_libs_OctoWS2811.html

*/
// Artnet is configured to use QNEthernet on Teensy.
#include "Artnet.h"
// not needed anymore: #include <SPI.h>
#include <OctoWS2811.h>
#include <EEPROM.h>

using namespace qindesign::network;

// i.e. LEDs per output.
#define LED_WIDTH 600

// i.e. how many strips; Octo board supports 8 channels out
#define LED_HEIGHT 8

#define version "2026.06.13"

// make sure the config above is correct for your setup. we expect the controlling
// software  to send (LED_HEIGHT * universesPerStrip) universes to this IP.
const int ledsPerUniverse = 170;

// Send fps timing to Serial out, should be around 40 fps
bool showFps = false;

// Custom Art-Net opcode for Bermuda alignment/control payloads.
// Art-Net opcodes are little-endian on the wire.
const uint16_t ART_BERMUDA_ALIGN = 0x7A01;

// how long is our update look taking to render?
// for reference: runs about 12us for regular, 32-universe code
// LD algorithm Q3-2023 was running 15-17us for 8-universe code
bool showTiming = false;

// @TODO maybe only enable this for the orange/purple brains?
bool serialVisualizerEnabled = false;

// ~~ end config ~~

// how many universes per strip?
const int universesPerStrip = 3;

const int maxUniverses = LED_HEIGHT * universesPerStrip;
// watch the logs and increase capacity if there are droped packets
const size_t artnetReceiveQueueCapacity = maxUniverses * 2;

const int numLeds = LED_WIDTH * LED_HEIGHT;
DMAMEM int displayMemory[LED_WIDTH * 6];
int drawingMemory[LED_WIDTH * 6];
const int config = WS2811_RGB | WS2811_800kHz;
OctoWS2811 leds(LED_WIDTH, displayMemory, drawingMemory, config);

// Artnet settings
Artnet artnet;

byte timeOffset = 0;

// used for test pattern, not Artnet.
byte ledsPerLayer[] = {
  72,
  66,
  60,
  54,
  48,
  45,
  39,
  33,
  27,
  21,
  15,
  12,
  6
};

// used for test pattern, not Artnet.
byte blanksPerLayer[] = {
  5,
  7,
  5,
  6,
  6,
  4,
  5,
  6,
  5,
  5,
  6,
  5,
  5
};

uint8_t layers = 13;

// used for data coming from Artnet. Remember that the way the triangle rows are
// arranged within the universes is complex (to reduce the number of universes sent)
//
// [universe, DMX starting channel, leds per layer, blanks per layer, adjustment]
int layerDescription[13][5] = {
  {0, 1, 72, 5, 0},
  {0, 217, 66, 7, 0},
  {1, 513, 60, 7, -2},
  {1, 693, 54, 6, 1},
  {1, 855, 48, 7, -1},
  {2, 1025, 45, 6, 0},
  {2, 1160, 39, 5, -1},
  {2, 1277, 33, 6, 1},
  {2, 1376, 27, 7, -1},
  {2, 1457, 21, 7, 2},
  {0, 415, 15, 7, 2},
  {0, 460, 12, 6, 2},
  {1, 999, 6, 5, 0}
};

// Per-triangle alignment offsets. Rows are triangles [0..7], columns are layers [0..12].
int8_t triangleAlignment[8][13] = {
  {0, 0, -2, 1, -1, 0, -1, 1, -1, 2, 2, 2, 0},
  {0, 0, -2, 1, -1, 0, -1, 1, -1, 2, 2, 2, 0},
  {0, 0, -2, 1, -1, 0, -1, 1, -1, 2, 2, 2, 0},
  {0, 0, -2, 1, -1, 0, -1, 1, -1, 2, 2, 2, 0},
  {0, 0, -2, 1, -1, 0, -1, 1, -1, 2, 2, 2, 0},
  {0, 0, -2, 1, -1, 0, -1, 1, -1, 2, 2, 2, 0},
  {0, 0, -2, 1, -1, 0, -1, 1, -1, 2, 2, 2, 0},
  {0, 0, -2, 1, -1, 0, -1, 1, -1, 2, 2, 2, 0},
};

namespace Alignment {
  const uint8_t TRIANGLES = 8;
  const uint8_t LAYERS = 13;
  const uint16_t ALIGNMENT_BYTES = TRIANGLES * LAYERS;
  const uint16_t EEPROM_MAGIC_ADDR = 0;
  const uint16_t EEPROM_DATA_ADDR = EEPROM_MAGIC_ADDR + sizeof(uint32_t);
  const uint32_t EEPROM_MAGIC = 0xBADA5510;

  // 0: no alignment pattern
  // 1-8: show alignment pattern on a single triangle 1-8
  // 9: show alignment pattern on all triangles
  int alignmentSelection = 0;

  int _lookupAdjustment(int layer, int whichTriangle) {
    if (whichTriangle < 0 || whichTriangle >= 8 || layer < 0 || layer >= 13) {
      return 0;
    }
    return triangleAlignment[whichTriangle][layer];
  }

  bool loadFromEeprom() {
    uint32_t magic = 0;
    EEPROM.get(EEPROM_MAGIC_ADDR, magic);
    if (magic != EEPROM_MAGIC) {
      return false;
    }

    Serial.printf("PERSIST: EEPROM magic ok (0x%08lX). Loading alignment matrix...\n",
                  static_cast<unsigned long>(magic));

    int addr = EEPROM_DATA_ADDR;
    for (uint8_t t = 0; t < TRIANGLES; t++) {
      Serial.printf("PERSIST: EEPROM triangle %u = [", t);
      for (uint8_t l = 0; l < LAYERS; l++) {
        triangleAlignment[t][l] = static_cast<int8_t>(EEPROM.read(addr));
        Serial.print(triangleAlignment[t][l]);
        if (l + 1 < LAYERS) {
          Serial.print(", ");
        }
        addr++;
      }
      Serial.println("]");
    }

    return true;
  }

  void saveToEeprom() {
    EEPROM.put(EEPROM_MAGIC_ADDR, EEPROM_MAGIC);

    int addr = EEPROM_DATA_ADDR;
    for (uint8_t t = 0; t < TRIANGLES; t++) {
      for (uint8_t l = 0; l < LAYERS; l++) {
        EEPROM.update(addr, static_cast<uint8_t>(triangleAlignment[t][l]));
        addr++;
      }
    }
  }
}

namespace SerialVisualizerSender {
  int frameIdx = 504;

  void setup()
  {
    Serial1.begin(9600);   // Hardware Serial1 on pins 0 (TX) and 1 (RX)
    Serial.println("Serial visualizer sender ready.");
  }

  void send(uint8_t *frame) {
    int r = frame[frameIdx];
    int g = frame[frameIdx + 1];
    int b = frame[frameIdx + 2];
    // Serial.printf("Sending: %d,%d,%d\n", r, g, b);
    Serial1.printf("%d,%d,%d\n", r, g, b);
  }
}

namespace Pattern {

  const int BRIGHTNESS = 50; // out of 255
  int ticks = 0;

  long getLedColorHSV(byte h, byte s, byte v)
  {
    byte RedLight;
    byte GreenLight;
    byte BlueLight;
    // this is the algorithm to convert from RGB to HSV
    h = (h * 192) / 256;           // 0..191
    unsigned int i = h / 32;       // We want a value of 0 thru 5
    unsigned int f = (h % 32) * 8; // 'fractional' part of 'i' 0..248 in jumps

    unsigned int sInv = 255 - s; // 0 -> 0xff, 0xff -> 0
    unsigned int fInv = 255 - f; // 0 -> 0xff, 0xff -> 0
    byte pv = v * sInv / 256;    // pv will be in range 0 - 255
    byte qv = v * (256 - s * f / 256) / 256;
    byte tv = v * (256 - s * fInv / 256) / 256;

    switch (i)
    {
    case 0:
      RedLight = v;
      GreenLight = tv;
      BlueLight = pv;
      break;
    case 1:
      RedLight = qv;
      GreenLight = v;
      BlueLight = pv;
      break;
    case 2:
      RedLight = pv;
      GreenLight = v;
      BlueLight = tv;
      break;
    case 3:
      RedLight = pv;
      GreenLight = qv;
      BlueLight = v;
      break;
    case 4:
      RedLight = tv;
      GreenLight = pv;
      BlueLight = v;
      break;
    case 5:
      RedLight = v;
      GreenLight = pv;
      BlueLight = qv;
      break;
    }
    long rgb = 0;

    rgb += RedLight << 16;
    rgb += GreenLight << 8;
    rgb += BlueLight;
    return rgb;
  }


  void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, HIGH);
  }

  long _getLayerColor(uint8_t layer) {
    const int highlightedLayer = (ticks / 3) % (layers + 7);
    int distance = abs( (layer+2) - highlightedLayer );
    // Serial.printf("debug layer color (highlighted, layer, distance): %d, %d, %d\n", highlightedLayer, layer, distance);
    if (distance >= 3) {
      return getLedColorHSV(0, 0, 0);
    } else if (distance == 2) {
      return getLedColorHSV(ticks/4 % 256, 255, 25);
    } else if (distance == 1) {
      return getLedColorHSV(ticks/4 % 256, 255, 50);
    } else {
      return getLedColorHSV(ticks/4 % 256, 255, BRIGHTNESS);
    }
  }

  void _rippleIdentifyLayers() {
    uint16_t position = 0;
    for (int layer=0; layer<layers; layer++) {
      long color = _getLayerColor(layer);

      for (uint8_t j = 0; j < ledsPerLayer[layer]; j++) {
        for (int strip = 0; strip < LED_HEIGHT; strip++) {
          int period = (strip + 1) + 1; // (strip+1) colored pixels, then 1 black pixel
          if ((position % period) < (strip + 1)) {
            leds.setPixelColor(position + LED_WIDTH * strip, color);
          } else {
            leds.setPixelColor(position + LED_WIDTH * strip, 0);
          }
        }
        position++;
      }

      for (uint8_t j = 0; j < blanksPerLayer[layer]; j++) {
        for (int strip = 0; strip < LED_HEIGHT; strip++) {
          leds.setPixelColor(position + LED_WIDTH * strip, 0);
        }
        position++;
      }
    }

    leds.show();
  }

  int _countPreviousLeds(int layer) {
    int total = 0;
    for (int i=layer-1; i>= 0; i--) {
      total += ledsPerLayer[i];
      total += blanksPerLayer[i];
    }
    return total;
  }

  void _blankEverything() {
    for (int i=0; i<LED_HEIGHT*LED_WIDTH; i++) {
      leds.setPixelColor(i, getLedColorHSV(0, 0, 0)); // set to black
    }
  }

  void _doAlignmentPattern() {
    for (int t=0; t<LED_HEIGHT; t++) {
      // only show alignment value sometimes
      if (!(Alignment::alignmentSelection == (t+1) || Alignment::alignmentSelection == 9)) {
        continue;
      }
      int ledIdx = 0;
      for (int i=0; i<layers; i++) {

        int ledsPerLayer = layerDescription[i][2];
        int adjustment = Alignment::_lookupAdjustment(i, t);

        ledIdx = t*LED_WIDTH + _countPreviousLeds(i) + adjustment;

        for (int led = 0; led < ledsPerLayer; led++) {
          // see if LED is within 3 pixels of the midpoint of ledsPerLayer
          int midpoint = ledsPerLayer / 2;
          if (abs(led - midpoint) <= 3) {
            leds.setPixelColor(ledIdx, getLedColorHSV(0, 255, BRIGHTNESS));
            // leds.setPixelColor(ledIdx, getLedColorHSV(0, 255, BRIGHTNESS));
          } else {
            leds.setPixelColor(ledIdx, getLedColorHSV(0, 0, 0)); // set to black
          }
          ledIdx++;
        }
      }
    }


    leds.show();
  }

  void loop()
  {
    _rippleIdentifyLayers();
    ticks++;
  }

  void intro() {
    _rippleIdentifyLayers();
  }
}

namespace Networking {
  // Teensy serial to IP address
  int _macToIpPairs[][2] = {
    {0xCB, 31}, // 00-15-B5-CB red i.e. "top"
    {0xDA, 32}, // 00-10-16-DA orange
    {0xFE, 32}, // 00-0C-35-FE silver (general prototyping)
    {0xF4, 32}, // 00-0C-35-FE silver (general prototyping)
    {0x18, 32}, // 00-0C-35-FE silver (backup from Bermuda bin)
    {0x9D, 32}, // LED door
    {0x5E, 33}, // 00-0C-46-5E yellow
    {0x5D, 34}, // 00-0C-46-5D green - motherbrain
    {0x92, 35}, // 00-0C-46-92 blue
    {0x70, 36}, // 00-0C-46-70 purple
  };
  const byte pairs = sizeof(_macToIpPairs) / sizeof(_macToIpPairs[0]);

  // Change ip for your setup, last octet is changed in updateIp()
  byte _ip[] = {169, 254, 18, 0};

  // have we received data for each universe?
  bool universesReceived[maxUniverses];

  // for calculating data received rates
  int universesReceivedTotal[maxUniverses];
  bool sendFrame = 1;

  // true once we have received an Artnet packet
  bool hasReceivedArtnetPacket = false;

  // true once UDP listener has started for Art-Net packets
  bool isArtnetListening = false;

  // frame time in ms, using millis()
  uint32_t _frameMs = 0;

  void networkChanged(bool hasIP, bool linkState) {
    if (!hasIP || !linkState) {
      if (isArtnetListening) {
        Serial.println("STATUS: Network unavailable; pausing Artnet listener.");
      }
      isArtnetListening = false;
      hasReceivedArtnetPacket = false;
      memset(universesReceived, 0, maxUniverses);
      return;
    }

    if (isArtnetListening) {
      return;
    }

    artnet.begin();
    isArtnetListening = true;
    Serial.println("STATUS: Listening for Artnet data.");
    Serial.print("INFO:   Local ip: ");
    Serial.println(Ethernet.localIP());
  }
  // In this fn, we use the hardware MAC from QNEthernet and map the last byte
  // to the desired static IP. Update the lookup table for new hardware.
  void updateIp()
  {
    uint8_t mac[6];
    Ethernet.macAddress(mac);
    Serial.printf("INFO:   MAC address: %02X:%02X:%02X:%02X:%02X:%02X\n",
                  mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

    for (int i=0; i<pairs; i++) {
      if (_macToIpPairs[i][0] == mac[5]) {
        Serial.println("INFO:   Used MAC to figure out which brain I am.");
        _ip[3] = _macToIpPairs[i][1];
      }
    }
  }

  // for a given layer, sum LEDs up to this layer
  int _countPreviousLeds(int layer) {
    int total = 0;
    for (int i=layer-1; i>= 0; i--) {
      total += ledsPerLayer[i];
      total += blanksPerLayer[i];
    }
    return total;
  }

  void _copyFrameToLeds(uint8_t *frame, int len, int ledIdx, int frameIdx) {
    for (int i=0; i<len; i++) {
      leds.setPixel(
        ledIdx+i,
        frame[frameIdx + 3*i],
        frame[frameIdx + 3*i+1],
        frame[frameIdx + 3*i+2]
      );
    }
  }

  void _updateLedRow(uint8_t *frame, int layer, int uni, int dmxPosition, int adjustment) {
    int uniOffset = uni % 3;
    int panelOffset = floor(uni / 3) * LED_WIDTH;
    // Serial.printf("Using offset %d for universe %d\n", panelOffset, uni);
    return _copyFrameToLeds(
      frame,
      layerDescription[layer][2],
      panelOffset + _countPreviousLeds(layer) + adjustment,
      dmxPosition - uniOffset*512 - 1
    );
  }

  void updateLeds(int uni) {
    uint8_t *frame = artnet.getDmxFrame();

    // consider update serial visualizer
    if (uni == 0 && serialVisualizerEnabled) {
      SerialVisualizerSender::send(frame);
    }

    int uniOffset = uni % 3;
    int whichTriangle = uni / 3;

    for (int i=0; i<layers; i++) {
      int uniFromDescription = layerDescription[i][0];
      if (uniFromDescription != uniOffset) {
        // why?? does this happen?
        continue;
      }

      int dmxPosition = layerDescription[i][1];

      int adjustment = Alignment::_lookupAdjustment(i, whichTriangle);
      // int adjustment = layerDescription[i][4];
      _updateLedRow(frame, i, uni, dmxPosition, adjustment);
    }

    if (Alignment::alignmentSelection > 0) {
      Pattern::_doAlignmentPattern();
    }
  }


  // https://www.arduino.cc/reference/en/libraries/ethernet/
  void setup()
  {
    artnet.setReceiveQueueCapacity(artnetReceiveQueueCapacity);
    Networking::updateIp();
    Serial.printf("INFO:   ArtNet UDP queue capacity: %u packets\n",
                  static_cast<unsigned>(artnet.receiveQueueCapacity()));

    EthernetHardwareStatus hwStatus = Ethernet.hardwareStatus();
    if (hwStatus == EthernetNoHardware) {
      Serial.println("ERROR:  Ethernet shield was not found.");
    }
    else if (hwStatus == EthernetW5100) {
      Serial.println("INFO:  W5100 Ethernet controller detected.");
    }
    else if (hwStatus == EthernetW5200) {
      Serial.println("INFO:   W5200 Ethernet controller detected.");
    }
    else if (hwStatus == EthernetW5500) {
      Serial.println("INFO:   W5500 Ethernet controller detected.");
    }
    else if (hwStatus == EthernetTeensy41) {
      Serial.println("INFO:   Teensy 4.1 native Ethernet detected.");
    }

    Ethernet.onLinkState([](bool state) {
      Serial.printf("[Ethernet] Link %s\n", state ? "ON" : "OFF");
      Networking::networkChanged(Ethernet.localIP() != INADDR_NONE, state);
    });

    Ethernet.onAddressChanged([]() {
      IPAddress ip = Ethernet.localIP();
      bool hasIP = (ip != INADDR_NONE);
      if (hasIP) {
        Serial.printf("[Ethernet] IP = %u.%u.%u.%u\n", ip[0], ip[1], ip[2], ip[3]);
      } else {
        Serial.println("[Ethernet] No IP address.");
      }
      Networking::networkChanged(hasIP, Ethernet.linkState());
    });

    Serial.println("INFO:   Starting QNEthernet with static IP...");
    IPAddress localIP(_ip[0], _ip[1], _ip[2], _ip[3]);
    IPAddress subnetMask(255, 255, 255, 0);
    IPAddress gateway(_ip[0], _ip[1], _ip[2], 1);
    if (!Ethernet.begin(localIP, subnetMask, gateway)) {
      Serial.println("ERROR:  Failed to start Ethernet.");
      Serial.println("ERROR:  Networking startup failed; waiting for retry/reboot.");
      return;
    }

    Networking::networkChanged(Ethernet.localIP() != INADDR_NONE,
                               Ethernet.linkState());
  }


  // print fps and how many frames we've received from each universe. this
  // prints incrementally (every 100 frames, when universe 0 is received)
  void printFps() {
    int uni = artnet.getUniverse();
    if (uni == 0 && universesReceivedTotal[0] % 100 == 0) {
      // check timing, do fps
      uint32_t currentTiming = millis();
      if (_frameMs > 0)
      {
        float fps = 100000. / (currentTiming - _frameMs);
        Serial.printf("PERF:   %2.2f fps.  ", fps);
      }
      _frameMs = currentTiming;

      // print how many frames we got from each universe
      for (int i = 0; i < maxUniverses; i++)
      {
        Serial.print(i);
        Serial.print(": ");
        //float pct = 100 * universesReceivedTotal[i] / universesReceivedTotal[0];
        float pct = universesReceivedTotal[i];
        Serial.print(pct, 2);
        Serial.print(" ");
      }

      // UDP receive queue telemetry helps tune artnetReceiveQueueCapacity.
      Serial.printf("| UDP q=%u/%u dropped=%lu total=%lu",
                    static_cast<unsigned>(artnet.receiveQueueSize()),
                    static_cast<unsigned>(artnet.receiveQueueCapacity()),
                    static_cast<unsigned long>(artnet.droppedReceiveCount()),
                    static_cast<unsigned long>(artnet.totalReceiveCount()));
      Serial.print("\n");
    }
  }

  void handleDmxFrame()
  {
    int uni = artnet.getUniverse();

    if (uni >= maxUniverses) {
      return;
    }


    // tracking
    universesReceived[uni] = 1;
    universesReceivedTotal[uni] = universesReceivedTotal[uni] + 1;

    if (showFps) {
      Networking::printFps();
    }

    // flash LED along with received data
    if (uni == 0 && universesReceivedTotal[0] % 30 == 0) {
      if (uni == 0 && universesReceivedTotal[0] % 60 == 0) {
        digitalWrite(LED_BUILTIN, HIGH);
      } else {
        digitalWrite(LED_BUILTIN, LOW);
      }
    }

    // how many microseconds to perform these operations for one Artnet frame?
    if (showTiming) {
      uint32_t beginTime = micros();
      updateLeds(uni);
      uint32_t elapsedTime = micros() - beginTime;
      Serial.printf("PERF:   elapsed microseconds: %lu \n", elapsedTime);
    } else {
      updateLeds(uni);
    }

    // if we've received data for each universe, call leds.show()

    sendFrame = 1;
    for (int i = 0; i < maxUniverses; i++)
    {
      if (universesReceived[i] == 0)
      {
        // Serial.printf("sendFrame is 0 on universe: %d (of %d)\n", i, maxUniverses);
        sendFrame = 0;
        break;
      }
    }

    if (sendFrame)
    {
      // Serial.println("calling leds.show()");
      leds.show();
      memset(universesReceived, 0, maxUniverses);
    }
  }

  void setHasReceivedArtnetPacket() {
    if (!Networking::hasReceivedArtnetPacket)
    {
      Serial.println("STATUS: Receiving network control data.");
      Networking::hasReceivedArtnetPacket = true;
      // black out each LED once when network control starts
      for (int i = 0; i < numLeds; i++)
      {
        leds.setPixel(i, 0, 0, 0);
      }
      leds.show();
    }
  }

  void logCustomArtPacket(uint16_t opcode) {
    uint16_t packetSize = artnet.getPacketSize();
    uint8_t *payload = artnet.getPacketPayload();

    // Payload format:
    // [0]     triangle_idx (0..7 update, 8 = disable test pattern)
    // [1..13] 13 signed alignment values for triangle 0..7
    const uint16_t expectedUpdatePayloadBytes = 14;
    const uint16_t artNetHeaderBytes = 10;
    if (packetSize < artNetHeaderBytes + 1) {
      Serial.printf(
        "CUSTOM: opcode=0x%04X packet too short (%u bytes, need >= %u)\n",
        opcode,
        packetSize,
        artNetHeaderBytes + 1
      );
      return;
    }

    uint8_t triangleIdx = payload[0];

    if (triangleIdx == 8) {
      Alignment::alignmentSelection = 0;
      Serial.printf("CUSTOM: opcode=0x%04X triangle_idx=8 -> test pattern OFF\n", opcode);
      Alignment::saveToEeprom();
      Serial.println("PERSIST: Saved alignment matrix to EEPROM.");
      Pattern::_blankEverything();
      leds.show();
      return;
    }

    if (triangleIdx > 7) {
      Serial.printf("CUSTOM: opcode=0x%04X invalid triangle_idx=%u (expected 0..8)\n", opcode, triangleIdx);
      return;
    }

    if (packetSize < artNetHeaderBytes + expectedUpdatePayloadBytes) {
      Serial.printf(
        "CUSTOM: opcode=0x%04X packet too short for update (%u bytes, need >= %u)\n",
        opcode,
        packetSize,
        artNetHeaderBytes + expectedUpdatePayloadBytes
      );
      return;
    }

    Alignment::alignmentSelection = 9;
    Serial.printf("CUSTOM: opcode=0x%04X triangle_idx=%u alignment=[", opcode, triangleIdx);
    for (uint8_t i = 0; i < 13; i++) {
      int8_t signedVal = static_cast<int8_t>(payload[i + 1]);
      triangleAlignment[triangleIdx][i] = signedVal;
      Serial.print(signedVal);
      if (i < 12) {
        Serial.print(", ");
      }
    }
    Serial.println("]");

    // Apply the updated alignment visually right away, even before DMX arrives.
    Pattern::_doAlignmentPattern();
  }

  void loop() {
    if (isArtnetListening) {
      uint16_t r = artnet.read();
      if (r == ART_DMX) {
        Networking::setHasReceivedArtnetPacket();
        Networking::handleDmxFrame();
      } else if (r == ART_BERMUDA_ALIGN) {
        Networking::setHasReceivedArtnetPacket();
        Networking::logCustomArtPacket(r);
      }
    }
  }
}

void setup()
{
  Serial.begin(115200);
  delay(2000);
  Serial.printf("INFO:   Version: %s\n", version);
  Serial.printf("INFO:   LED counter: %d pixels, %d LEDs \n", leds.numPixels(), numLeds);
  Serial.println();

  if (Alignment::loadFromEeprom()) {
    Serial.println("PERSIST: Restored alignment matrix from EEPROM.");
  } else {
    Serial.println("PERSIST: No saved alignment found; using compiled defaults.");
  }

  leds.begin();
  Pattern::setup();
  Pattern::intro();

  if (serialVisualizerEnabled) {
    SerialVisualizerSender::setup();
  }

  Networking::setup();
}



void loop()
{
  Networking::loop();


  if (!Networking::hasReceivedArtnetPacket)
  {
    Pattern::loop();
  }
}
