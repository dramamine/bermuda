"""
CHOP Execute DAT

me - this DAT

Make sure the corresponding toggle is enabled in the CHOP Execute DAT.
"""
playlist = mod("/project1/ui_container/playlist_manager/playlist_container/playlist_music_exec")


def onValueChange(channel: Channel, sampleIndex: int, val: float,
                  prev: float):
	# print(f"audio_info_exec::onValueChange channel={channel.name} val={val} prev={prev}")
	if val >= 1.0:
		is_toggle_on = op('playlist_toggle').par.Value0.eval()
		if is_toggle_on:
			playlist.next_track()
	return
