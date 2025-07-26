## What's going on here?

Beat Link Trigger is listening for phrase information, etc.

The file bermuda-show.bls contains the stuff below. You should be able to recreate the .bls file from these functions.


### bermuda-show Shared functions

```lua
(defn send-json-to-touchdesigner
  "Encodes a map as JSON and sends it in a UDP packet
  to TouchDesigner."
  [globals m]
  (let [message (str (cheshire.core/encode m) "\n")  ; Encode as JSON line.
       {:keys [td-address td-port td-socket]} @globals  ; Find where to send.
       data (.getBytes message)  ; Get JSON as raw byte array.
       packet (java.net.DatagramPacket. data (count data) td-address td-port)]
  (.send td-socket packet)))
```

### bermuda-show Global Setup Expression

```lua
;; Create a socket for sending UDP to TouchDesigner, and record the
;; address and port to which such UDP messages should be sent.
(swap! globals assoc :td-socket (java.net.DatagramSocket.))
(swap! globals assoc :td-address (java.net.InetAddress/getLocalHost))
(swap! globals assoc :td-port 7000)
```

### bermuda-show Beat Expression for Phrase Trigger "Phrase 1"

```lua
(let [payload {"masterPlayerNumber" device-number
               "bpm"                effective-tempo
               "trackBank"          track-bank
               "phraseType"         phrase-type
               "trackArtist"        track-artist
               "trackTimeReached"   track-time-reached
               "trackBpm"           track-bpm
               "trackTitle"         track-title
               "beat"               beat-within-bar
               "fill"               (= section :fill)}]
  (send-json-to-touchdesigner globals payload))
```
