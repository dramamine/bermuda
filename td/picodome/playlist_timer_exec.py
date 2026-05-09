# me is this DAT.
# timerOp is the connected Timer CHOP.
# cycle is the cycle index.
# segment is the segment index.
# fraction is the time in fractional form.
#
# interrupt is True if the user initated a premature
# interrupt, False if a result of normal timeout.


def onDone(timerOp, segment, interrupt):
	# No longer used â€” track end is detected by audio_info_exec.py
	return
