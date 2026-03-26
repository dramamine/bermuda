# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
#
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.
import selected_csv_exec as scripts


def onValueChange(par, prev):
	if par.eval():
		scripts.load_current_song()
	else:
		scripts.stop_playback()
	return
