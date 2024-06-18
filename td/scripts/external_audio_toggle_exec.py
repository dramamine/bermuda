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
		# external audio on
		# first, turn off playlist
		op('toggle').par.Value0 = False
		# op('/project1/ui_container/playlist_container/audio_analysis_and_player/audiofilein1').par.play = False
		# mod("/project1/ui_container/resolume_container/sld_resolume_controller").set_is_playlist_audio(False)

		# then, turn on external audio
		op('/project1/ui_container/playlist_container/audio_analysis_and_player/switch2').par.index = 1
		op('/project1/ui_container/playlist_container/audio_analysis_and_player/audiodevin1').bypass = 0


		scripts.play_song()
	else:
		# turn off external audio
		# op('/project1/ui_container/playlist_container/audio_analysis_and_player').par.Value0 = False
		# op('/project1/ui_container/playlist_container/audio_analysis_and_player/switch2').par.index = 0
		# mod("/project1/ui_container/resolume_container/sld_resolume_controller").set_is_playlist_audio(True)
		op('/project1/ui_container/playlist_container/audio_analysis_and_player/audiodevin1').bypass = 1

		# op('/project1/ui_container/playlist_container/audio_analysis_and_player/audiofilein1').par.play = False
		# op('/project1/ui_container/playlist_container/audio_analysis_and_player/switch2').par.index = 1
		# mod("/project1/ui_container/resolume_container/sld_resolume_controller").set_is_playlist_audio(False)
		# scripts.reset_timecode()
	return
