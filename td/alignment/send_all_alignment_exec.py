"""
CHOP Execute DAT

me - this DAT

Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
"""


def _get_send_module():
	mod_dat = op('send_values_toggle_exec')
	if mod_dat is None:
		debug('send_values_toggle_exec DAT not found; cannot send alignment data.')
		return None

	module = mod_dat.module
	if module is None:
		debug('send_values_toggle_exec module unavailable.')
		return None

	if not hasattr(module, 'send_all'):
		debug('send_values_toggle_exec missing send_all().')
		return None

	if not hasattr(module, 'turn_off_test_patterns'):
		debug('send_values_toggle_exec missing turn_off_test_patterns().')
		return None

	return module


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
	module = _get_send_module()
	if module is None:
		return

	# 1) Send all alignment rows.
	rows_sent = module.send_all(log_success=False)
	# 2) Then send test-pattern OFF to each unique IP.
	ips_sent = module.turn_off_test_patterns(log_success=False)
	debug('Send-all interaction: sent {} alignment rows, then test-pattern OFF to {} IP(s).'.format(
		rows_sent, ips_sent
	))
	return


def whileOn(channel: Channel, sampleIndex: int, val: float,
            prev: float):
	"""
	Called every frame while a channel is non-zero.
	
	Args:
		channel: The Channel object which has changed
		sampleIndex: The index of the changed sample
		val: The numeric value of the changed sample
		prev: The previous sample value
	"""
	return


def onOnToOff(channel: Channel, sampleIndex: int, val: float,
              prev: float):
	"""
	Called when a channel changes from non-zero to 0.
	
	Args:
		channel: The Channel object which has changed
		sampleIndex: The index of the changed sample
		val: The numeric value of the changed sample
		prev: The previous sample value
	"""
	return


def whileOff(channel: Channel, sampleIndex: int, val: float,
             prev: float):
	"""
	Called every frame while a channel is 0.
	
	Args:
		channel: The Channel object which has changed
		sampleIndex: The index of the changed sample
		val: The numeric value of the changed sample
		prev: The previous sample value
	"""
	return


def onValueChange(channel: Channel, sampleIndex: int, val: float,
                  prev: float):
	"""
	Called when a channel value changes.
	
	Args:
		channel: The Channel object which has changed
		sampleIndex: The index of the changed sample
		val: The numeric value of the changed sample
		prev: The previous sample value
	"""
	return
