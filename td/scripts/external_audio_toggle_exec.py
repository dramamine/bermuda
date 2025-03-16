# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
#
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.
# import selected_csv_exec as scripts


def onValueChange(par, prev):
	# use par.eval() to get current value
	if par.eval():
		# external audio on
		# first, turn off playlist
		op('/project1/ui_container/playlist_manager/playlist_toggle').par.Value0 = False
		# then, turn on external audio
		op('/project1/ui_container/playlist_container/audio_analysis_and_player/audiodevin1').bypass = 0
	else:
		# turn off external audio
		op('/project1/ui_container/playlist_container/audio_analysis_and_player/audiodevin1').bypass = 1
	return
