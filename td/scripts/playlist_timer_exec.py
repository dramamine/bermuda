# me is this DAT.
# timerOp is the connected Timer CHOP.
# cycle is the cycle index.
# segment is the segment index.
# fraction is the time in fractional form.
#
# interrupt is True if the user initated a premature
# interrupt, False if a result of normal timeout.
import selected_csv_exec as scripts


def onDone(timerOp, segment, interrupt):
	# print('playlist_timer::onDone() segment', segment)
	scripts.do_current_action()
	scripts.load_next_timer()

	return
