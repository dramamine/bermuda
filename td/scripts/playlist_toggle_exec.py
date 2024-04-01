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
		print("playlist_toggle_exec::toggled on")
		# turn off external audio
		op('/project1/ui_container/audio_container/toggle').par.Value0 = False
		op('audiofilein1').par.play = True
		mod("/project1/ui_container/resolume_container/sld_resolume_controller").set_is_playlist_audio(True)
		scripts.play_song()
	else:
		print("playlist_toggle_exec::toggled off")
		op('audiofilein1').par.play = False
		mod("/project1/ui_container/resolume_container/sld_resolume_controller").set_is_playlist_audio(False)
		scripts.reset_timecode()
	return
