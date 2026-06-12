# me - this DAT
#
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
#
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

import re
import struct


def get_active_alignment_map_row():
	lookup_name = op('triangle_idx')[1, 0].val
	alignment_map = op('alignment_map')

	if alignment_map is None:
		print("No alignment_map operator found")
		return None

	for r in range(1, alignment_map.numRows):
		if alignment_map[r, 'name'].val == lookup_name:
			return r

	print("No alignment_map row found for name:", lookup_name)
	return None


def update_alignment_map_value(row_idx, new_alignment_idx):
	alignment_map = op('alignment_map')
	if alignment_map is None:
		print("No alignment_map operator found")
		return None

	name = alignment_map[row_idx, 'name'].val

	alignment_map[row_idx, 'alignment_idx'] = new_alignment_idx
	alignment_idx = int(alignment_map[row_idx, 'alignment_idx'].val)
	return alignment_idx


def get_alignment_row_values(alignment_idx):
	alignment_options = op('alignment_options')
	if alignment_options is None:
		print("No alignment_options operator found")
		return None

	if alignment_idx < 0 or alignment_idx >= alignment_options.numRows:
		print("alignment_idx out of range:", alignment_idx)
		return None

	option_row = alignment_options.row(alignment_idx)
	if option_row is None or len(option_row) < 13:
		print("alignment_options row missing or does not have 13 columns:", alignment_idx)
		return None

	try:
		return [int(c.val) for c in option_row[:13]]
	except Exception as exc:
		print("Failed to parse alignment_options row as ints:", exc)
		return None


def get_triangle_digit_from_name(name):
	match = re.search(r'\d+', str(name))
	if match is None:
		print("No numeric part found in name:", name)
		return None

	triangle_digit = int(match.group(0))
	if triangle_digit < 0 or triangle_digit > 7:
		print("Triangle digit out of expected range 0-7:", triangle_digit)
		return None

	return triangle_digit


def get_udp_from_ip(ip):
	ip_str = str(ip).strip()
	match = re.search(r'(\d)\D*$', ip_str)
	if match is None:
		print("Could not parse UDP output index from IP:", ip)
		return None

	udp_idx = int(match.group(1))
	if udp_idx < 1 or udp_idx > 6:
		print("Parsed UDP output index out of range 1-6 from IP:", ip)
		return None

	udp_name = 'udpout{}'.format(udp_idx)
	udp = op(udp_name)
	if udp is None:
		print("{} not found; cannot send packet for IP {}".format(udp_name, ip))
		return None

	return udp


def send_row_to_udp(row_idx):
	alignment_map = op('alignment_map')
	if alignment_map is None:
		print("No alignment_map operator found")
		return False

	ip = alignment_map[row_idx, 'ip'].val
	name = alignment_map[row_idx, 'name'].val
	alignment_idx = int(alignment_map[row_idx, 'alignment_idx'].val)

	alignment_values = get_alignment_row_values(alignment_idx)
	if alignment_values is None:
		return False

	udp = get_udp_from_ip(ip)
	if udp is None:
		return False

	triangle_digit = get_triangle_digit_from_name(name)
	if triangle_digit is None:
		return False

	payload_values = [triangle_digit] + alignment_values

	# Signed int8 packing allows the negative alignment offsets.
	try:
		payload = struct.pack('<{}b'.format(len(payload_values)), *payload_values)
	except Exception as exc:
		print("Failed to pack payload as signed bytes:", exc)
		return False

	packet = b'Art-Net\x00' + struct.pack('<H', 0x7A01) + payload
	udp.sendBytes(packet)
	print("UDP send: target={} ip={} bytes={}".format(udp.name, ip, list(packet)))
	return True


def onOffToOn(channel, sampleIndex, val, prev):
	return


def whileOn(channel, sampleIndex, val, prev):
	return


def onOnToOff(channel, sampleIndex, val, prev):
	return


def whileOff(channel, sampleIndex, val, prev):
	return


def onValueChange(channel, sampleIndex, val, prev):
	row_idx = get_active_alignment_map_row()
	if row_idx is None:
		return

	new_alignment_idx = int(val)
	alignment_idx = update_alignment_map_value(row_idx, new_alignment_idx)
	if alignment_idx is None:
		return

	if send_row_to_udp(row_idx):
		alignment_map = op('alignment_map')
		name = alignment_map[row_idx, 'name'].val
		ip = alignment_map[row_idx, 'ip'].val
		# print("Active value interaction: name={} ip={} alignment_idx={}".format(
		# 	name, ip, alignment_idx
		# ))

	return
