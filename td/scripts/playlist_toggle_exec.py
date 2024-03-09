# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
#
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.
import selected_csv_exec as scripts


def onValueChange(par, prev):
	# use par.eval() to get current value
	if par.eval():
		print("toggled on")
		# turn off external audio
		op('/project1/ui_container/audio_container/audio_toggle_exec').par.Value0 = False
		scripts.play_song()
	else:
		print("toggled off")
		scripts.reset_timecode()
	return
