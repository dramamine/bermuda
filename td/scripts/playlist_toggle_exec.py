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
		# print("playlist_toggle_exec::toggled on")
		# turn off external audio
		op("/project1/ui_container/audio_device_manager/audiodevin_ui/external_audio_toggle").par.Value0 = False

		op('/project1/ui_container/playlist_container/audio_analysis_and_player/switch2').par.index = 0
		op('/project1/ui_container/playlist_container/audio_analysis_and_player/audiofilein1').par.play = True
		mod("/project1/ui_container/resolume_container/sld_resolume_controller").set_is_playlist_audio(True)
		scripts.load_current_song()
	else:
		# print("playlist_toggle_exec::toggled off")
		op('/project1/ui_container/playlist_container/audio_analysis_and_player/audiofilein1').par.play = False
		op('/project1/ui_container/playlist_container/audio_analysis_and_player/switch2').par.index = 1
		mod("/project1/ui_container/resolume_container/sld_resolume_controller").set_is_playlist_audio(False)
		op('/project1/ui_container/playlist_manager/timer1').par.initialize.pulse()

		scripts.reset_timecode()
	return
