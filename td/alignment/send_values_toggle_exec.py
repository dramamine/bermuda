# me - this DAT
#
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
#
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

import struct

ARTNET_HEADER = b'Art-Net\x00'
ART_BERMUDA_ALIGN = 0x7A01


def _get_update_alignment_module():
	helper_dat = op('update_alignment_value')
	if helper_dat is None:
		debug('update_alignment_value DAT not found; cannot send alignment data.')
		return None

	helper_mod = helper_dat.module
	if helper_mod is None:
		debug('update_alignment_value module unavailable; cannot send alignment data.')
		return None

	return helper_mod


def send_all(log_success=True):
	alignment_map = op('alignment_map')
	if alignment_map is None:
		debug('alignment_map not found; nothing sent.')
		return 0

	helper_mod = _get_update_alignment_module()
	if helper_mod is None:
		return 0

	sent = 0
	for row_idx in range(1, alignment_map.numRows):
		if helper_mod.send_row_to_udp(row_idx):
			sent += 1

	if log_success:
		debug('Send changes interaction: sent {} alignment packets.'.format(sent))
	return sent


def turn_off_test_pattern(ip):
	helper_mod = _get_update_alignment_module()
	if helper_mod is None:
		return False

	if not hasattr(helper_mod, 'get_udp_from_ip'):
		debug('update_alignment_value module missing get_udp_from_ip(ip).')
		return False

	udp = helper_mod.get_udp_from_ip(ip)
	if udp is None:
		debug('No UDP output found for IP {}; cannot send test-pattern OFF packet.'.format(ip))
		return False

	# triangle_idx=8 is firmware command to disable test pattern mode.
	payload = bytes([8])
	packet = ARTNET_HEADER + struct.pack('<H', ART_BERMUDA_ALIGN) + payload
	udp.sendBytes(packet)
	return True


def turn_off_test_patterns(log_success=True):
	alignment_map = op('alignment_map')
	if alignment_map is None:
		debug('alignment_map not found; cannot send test-pattern OFF packets.')
		return 0

	unique_ips = []
	seen = set()
	for row_idx in range(1, alignment_map.numRows):
		ip = str(alignment_map[row_idx, 'ip'].val).strip()
		if not ip or ip in seen:
			continue
		seen.add(ip)
		unique_ips.append(ip)

	sent = 0
	for ip in unique_ips:
		if turn_off_test_pattern(ip):
			sent += 1

	if log_success:
		debug('Send changes interaction: sent test-pattern OFF to {} unique IP(s).'.format(sent))
	return sent


def onOffToOn(channel, sampleIndex, val, prev):
	# reset()
	# mod('datexec1').onTableChange(None)
	sent = send_all(log_success=False)
	debug('Send changes interaction: ON -> sent {} alignment packets.'.format(sent))
	return


def whileOn(channel, sampleIndex, val, prev):
	return


def onOnToOff(channel, sampleIndex, val, prev):
	sent = turn_off_test_patterns(log_success=False)
	debug('Send changes interaction: OFF -> sent test-pattern OFF to {} unique IP(s).'.format(sent))

	return


def whileOff(channel, sampleIndex, val, prev):
	return


def onValueChange(channel, sampleIndex, val, prev):
	return
