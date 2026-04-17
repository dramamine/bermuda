"""
CHOP Execute DAT

me - this DAT

Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
"""


def onOffToOn(channel: Channel, sampleIndex: int, val: float,
              prev: float):
  print("test_pattern_exec: test mode ON")
  mod("triangle_pixelmap_generator").set_test_mode(True)
  return


def onOnToOff(channel: Channel, sampleIndex: int, val: float,
              prev: float):
  print("test_pattern_exec: test mode OFF")
  mod("triangle_pixelmap_generator").set_test_mode(False)
  return
