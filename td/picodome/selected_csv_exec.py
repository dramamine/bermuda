# me - this DAT.
#
# dat - the changed DAT
# rows - a list of row indices
# cols - a list of column indices
# cells - the list of cells that have changed content
# prev - the list of previous string contents of the changed cells
#
# Make sure the corresponding toggle is enabled in the DAT Execute DAT.
#
# If rows or columns are deleted, sizeChange will be called instead of row/col/cellChange.
import re


def onRowChange(dat, rows):
	is_toggle_on = op('playlist_toggle').par.Value0.eval()
	if not is_toggle_on:
		return

	mp3_path = str(dat[1, 1])
	mp3_path = re.sub(
		"E:/git/lightdream-scripts/td/",
		"",
		mp3_path
	)

	op('audiofilein1').par.file = mp3_path
	play_song()
	return

def load_current_song():
	onRowChange(op('selected_music'), None)
	return


def play_song():
	op('timecode1').par.init.pulse()
	op('timecode1').par.start.pulse()


def stop_playback():
	op('timecode1').par.init.pulse()
