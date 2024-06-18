# me - this DAT
#
# dat - the DAT that received the event
# rowIndex - the row number that was added
# message - a readable description of the event
# channel - the numeric value of the event channel
# index - the numeric value of the event index
# value - the numeric value of the event value
# input - true when the event was received
# bytes - a byte array of the received event
#
# Example:
# message  channel index value     bytes
# Note On  1        63   127       90 2f 127
ACTIVE_CLIPS_LIMIT = 3


def send(loc, val):
	op('../resolume_container/resolume').sendOSC(loc, [val])
	return


def effectBypass(name, val):
	send('/composition/layers/5/clips/1/video/effects/'+name+'/bypassed', val)
	return


def onReceiveMIDI(dat, rowIndex, message, channel, index, value, input, bytes):
	print('MIDI message:', message, channel, index, value, input, bytes)

	if channel == 3:

		if index >= 37 and index <= 48:
			return handleEffects(message, index)
		elif index >= 69 and index <= 80:
			return handleEffects(message, index)
		elif index >= 99:
			return handleTempo(message, index)
		return handleMasks(message, index)

	if channel == 6:
		return handleVideo(message, index)

	return


# /composition/layers/5/clips/1/video/effects/greenhousevideo/bypassed
effects_dict = {
	37: 'greenhousevideo',
	38: 'slide',
	39: 'slide2',
	40: 'slide3',
	41: 'slide4',
	42: 'huerotate',
	43: 'suckr',
	44: 'threshold',

	45: 'threshold2',
	46: 'threshold3',
	47: 'vignette',
	48: 'blow',

	69: 'edgedetection',
	70: 'ezradialcloner',
	71: 'ezradialcloner2',
	72: 'goo',
	73: 'gridcloner',
	74: 'heat',
	75: 'heat2',
	76: 'infinitezoom',
	77: 'kaleidoscope',
	78: 'kaleidoscope2',
	79: 'kaleidoscope3',
	80: 'linearcloner',

	# extras; TODO sub out ones above that arent so good
	96: 'mirror',
	97: 'polarkaleido',
	98: 'polarkaleido2',
	99: 'polarkaleido3',
	100: 'polarkaleido4',
}


def handleEffects(message, index):
	val = 0 if message == 'Note On' else 1
	if index in effects_dict:
		effectBypass(effects_dict[index], val)
	return


active = 0
active_mask = 0
active_bg = 0
active_dict = {}


def handleMasks(message, index):
	global active, active_dict, active_bg, active_mask

	bgoffset = 64
	maskindex = 0
	blockindex = 0
	if index >= 49 and index <= 52:
		maskindex = index - 48
		blockindex = 1
	elif index >= 81 and index <= 84:
		maskindex = index - 80 + 4
		blockindex = 2
	elif index >= 53 and index <= 60:
		maskindex = index - 52 + 8
		blockindex = 3
	elif index >= 61 and index <= 68:
		maskindex = index - 52 + 8 + 8
		blockindex = 32
	elif index >= 85 and index <= 92:
		maskindex = index - 84 + 24 - 8
		blockindex = 4
	elif index >= 93 and index <= 100:
		maskindex = index - 84 + 24
		blockindex = 42

	print("maskindex:", maskindex, "blockindex:", blockindex, "midinote", index)

	if maskindex == 0:
		return

	if message == 'Note On':
		if active >= ACTIVE_CLIPS_LIMIT:
			return

		op('mask'+str(maskindex)).bypass = False
		active += 1
		active_mask += 1
		active_dict[maskindex] = True

	elif message == 'Note Off':
		op('mask'+str(maskindex)).bypass = True
		if active_dict[maskindex] == True:
			active -= 1
			active_mask -= 1

			active_dict[maskindex] = False

	# dummy white so that multiplying by bg == bg
	op('constant1').bypass = (active_mask > 0)

	# masking solo
	op('constant2').bypass = op('thresh1').bypass = op(
		'math1').bypass = not (active_bg == 0 and active_mask > 0)

	# nothing active
	op('bgcomp1').bypass = active_bg == 0 and active_mask == 0

	print("active counts:", active_bg, active_mask, active)

def handleVideo(message, index):
	global active, active_dict, active_bg, active_mask

	bgoffset = 64
	bgindex = 0
	maskindex = 0
	if index >= 37 and index <= 52:
		bgindex = index - 36
	elif index >= 69 and index <= 84:
		bgindex = index - (68-16)
	elif index >= 53 and index <= 68:
		bgindex = index - 20
	elif index >= 85 and index <= 100:
		bgindex = index - (84-48)

	print("bgindex:", bgindex, "midinote", index)

	# deprecated probably
	if maskindex > 0:
		if message == 'Note On':
			if active >= ACTIVE_CLIPS_LIMIT:
				return

			op('mask'+str(maskindex)).bypass = False
			active += 1
			active_mask += 1
			active_dict[maskindex] = True

		elif message == 'Note Off':
			op('mask'+str(maskindex)).bypass = True
			if active_dict[maskindex] == True:
				active -= 1
				active_mask -= 1

				active_dict[maskindex] = False

	if bgindex > 0:
		if message == 'Note On':
			if active >= ACTIVE_CLIPS_LIMIT:
				return

			op('bg'+str(bgindex)).bypass = False
			active += 1
			active_bg += 1
			active_dict[bgindex+bgoffset] = True

		elif message == 'Note Off':
			op('bg'+str(bgindex)).bypass = True
			if active_dict[bgindex+bgoffset] == True:
				active -= 1
				active_bg -= 1
				active_dict[bgindex+bgoffset] = False

	# dummy white so that multiplying by bg == bg
	op('constant1').bypass = (active_mask > 0)

	# masking solo
	op('constant2').bypass = op('thresh1').bypass = op(
		'math1').bypass = not (active_bg == 0 and active_mask > 0)

	# nothing active
	op('bgcomp1').bypass = active_bg == 0 and active_mask == 0

	print("active counts:", active_bg, active_mask, active)

	return

def handleTempo(message, index):
	if index == 99:
		if message == 'Note On':
			print("tempo tap")
			return send('/composition/tempocontroller/tempotap', 1)
		else:
			return send('/composition/tempocontroller/tempotap', 0)

	print("midi load pattern and play")
	# index 102
	if message == 'Note On':
		bpm_from_resolume = op("/project1/ui_container/resolume_container/resolume_bpm")[0, 0]
		print("bpm_from_resolume:", bpm_from_resolume)
		op("/project1/ui_container/resolume_container/bpm").par.Value0 = bpm_from_resolume
		# mod("/project1/ui_container/resolume_container/sld_resolume_controller").load_pattern_and_play()
	return
