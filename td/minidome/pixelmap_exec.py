"""
CHOP Execute DAT

me - this DAT

Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
"""


def onOffToOn(channel: Channel, sampleIndex: int, val: float,
              prev: float):
	"""
	Called when a channel changes from 0 to non-zero.

	Args:
		channel: The Channel object which has changed
		sampleIndex: The index of the changed sample
		val: The numeric value of the changed sample
		prev: The previous sample value
	"""
	mod("triangle_pixelmap_generator").generate_panel_map()
	return
