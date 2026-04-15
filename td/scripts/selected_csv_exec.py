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
import time
current_event_ts = '0.000'

# If True, start/stop Resolume's video recorder with each song
use_video_recorder = True


def onRowChange(dat, rows):
	# print("selected_csv_exec::row has changed.", rows)

	is_toggle_on = op('playlist_toggle').par.Value0.eval()
	if not is_toggle_on:
		return

	mp3_path = str(dat[1, 1])
	# remove "E:/git/lightdream-scripts/td/" from path
	mp3_path = re.sub(
		"E:/git/lightdream-scripts/td/",
		"",
		mp3_path
	)

	op('/project1/ui_container/playlist_container/audio_analysis_and_player/audiofilein1').par.file = mp3_path

	csv_path = re.sub(
		r'/\d{2}\s',
		"/",
		re.sub(
			r'(mp3|m4a)',
			"csv",
			mp3_path
		)
	)


	op('text1').par.file = csv_path
	play_song()

	return

def load_current_song():
	print("selected_csv_exec::reset_timecode: load current song called")
	onRowChange(op('selected_music'), None)
	return


def play_song():
	print("selected_csv_exec::play_song: starting song, setting up first timer event")
	op('/project1/ui_container/playlist_container/audio_analysis_and_player/timecode1').par.init.pulse()
	op('/project1/ui_container/playlist_container/audio_analysis_and_player/timecode1').par.start.pulse()
	if use_video_recorder:
		mod("/project1/ui_container/resolume_container/sld_resolume_commands").record(True)
	load_next_timer(use_zero=True)
	pass


def reset_timecode():
	print("selected_csv_exec::reset_timecode: resetting timecode and stopping timer")
	op('/project1/ui_container/playlist_container/audio_analysis_and_player/timecode1').par.init.pulse()
	op('timer1').par.initialize.pulse()
	return

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def get_csv_rows():
	"""Parse text1 DAT into a list of rows, each row split by comma. Skips header and empty rows."""
	raw = str(op('text1').rows()[0][0])
	lines = raw.split('\n')
	rows = []
	for line in lines[1:]:  # skip header
		line = line.strip()
		if not line:
			continue
		cols = line.split(',')
		rows.append(cols)
	return rows

def do_current_action():
	global current_event_ts

	if current_event_ts == '__recording_end__':
		print("selected_csv_exec::do_current_action: recording end, stopping recorder, waiting 30s before next track")
		if use_video_recorder:
			mod("/project1/ui_container/resolume_container/sld_resolume_commands").record(False)
		current_event_ts = '__song_end__'
		op('timer1').par.length = 30
		op('timer1').par.initialize.pulse()
		op('timer1').par.start.pulse()
		return

	if current_event_ts == '__song_end__':
		print("selected_csv_exec::do_current_action: song ended, advancing to next track")
		mod("/project1/ui_container/playlist_manager/playlist_container/playlist_music_exec").next_track()
		return

	csv_rows = get_csv_rows()
	found_match = False

	for row in csv_rows:
		event_ts = row[0] if len(row) > 0 else ''
		if (current_event_ts != event_ts):
			continue

		found_match = True
		current_action = row[1] if len(row) > 1 else ''
		value1 = row[2] if len(row) > 2 else ''
		value2 = row[3] if len(row) > 3 else ''
		value3 = row[4] if len(row) > 4 else ''

		# print(f"selected_csv_exec::TRIGGERED EVENT ts={event_ts} action={current_action} v1={value1} v2={value2} v3={value3}")
		print("selected_csv_exec:current action:", current_action, value1, value2, value3)

		if current_action == "set_intensity":
			mod("/project1/ui_container/resolume_container/sld_resolume_controller").choose_intensity(int(value1))
			mod("/project1/ui_container/resolume_container/sld_resolume_controller").load_pattern_and_play()
		elif current_action == "set_bpm":
			op("/project1/ui_container/resolume_container/bpm").par.Value0 = float(value1)
			mod("/project1/ui_container/resolume_container/sld_resolume_controller").on_bpm_change(float(value1), restart_section=False, resync=True)
		elif current_action == "update_section":
			intensity = safe_cast(value1, int, None)
			transition_style = safe_cast(value2, str, '')
			transition_time = safe_cast(value3, int, 2)

			if (transition_style == "fadeout"):
				mod("/project1/ui_container/resolume_container/sld_resolume_controller").fadeout(transition_time)
			elif (transition_style == "fadein"):
				mod("/project1/ui_container/resolume_container/sld_resolume_commands").update_transition_time(1, 0)
				mod("/project1/ui_container/resolume_container/sld_resolume_commands").update_transition_time(2, 0)
				mod("/project1/ui_container/resolume_container/sld_resolume_commands").update_transition_time(3, 0)
				mod("/project1/ui_container/resolume_container/sld_resolume_commands").clear()
				mod("/project1/ui_container/resolume_container/sld_resolume_controller").choose_intensity(intensity)
				mod("/project1/ui_container/resolume_container/sld_resolume_controller").load_pattern_and_play(transition_time)
			elif (transition_style == "sudden"):
				mod("/project1/ui_container/resolume_container/sld_resolume_commands").update_transition_time(1, 0)
				mod("/project1/ui_container/resolume_container/sld_resolume_commands").update_transition_time(2, 0)
				mod("/project1/ui_container/resolume_container/sld_resolume_commands").update_transition_time(3, 0)
				mod("/project1/ui_container/resolume_container/sld_resolume_controller").choose_intensity(intensity)
				mod("/project1/ui_container/resolume_container/sld_resolume_controller").load_pattern_and_play()
			else:
				mod("/project1/ui_container/resolume_container/sld_resolume_controller").choose_intensity(intensity)
				mod("/project1/ui_container/resolume_container/sld_resolume_controller").load_pattern_and_play()

		elif current_action == "end":
			mod("/project1/ui_container/playlist_manager/playlist_container/playlist_music_exec").next_track()
		elif current_action == "phrase_change":
			mod("/project1/ui_container/pioneer_link/pioneer_exec").onCellChange(op('pioneer_data'), [value1], [], sync_bpm=False)
			mod("/project1/ui_container/resolume_container/sld_resolume_commands").resync()

	if not found_match:
		print("selected_csv_exec::do_current_action WARNING: no matching event for ts", current_event_ts)
	load_next_timer()
	return


def load_next_timer(use_zero=False):
	global current_event_ts
	# read timestamp
	ts = 0 if use_zero else op('/project1/ui_container/playlist_container/audio_analysis_and_player/timecode1')['total_seconds']
	csv_rows = get_csv_rows()

	# get next upcoming event
	found_next = False
	for row in csv_rows:
		event_ts = float(row[0])
		if event_ts > (ts + 0.005):
			timer_length = event_ts - ts
			current_event_ts = row[0]

			# set timer
			op('timer1').par.length = timer_length
			op('timer1').par.initialize.pulse()
			op('timer1').par.start.pulse()
			found_next = True
			break
	if not found_next:
		info = op('/project1/ui_container/playlist_container/audio_analysis_and_player/audiofilein1_info')
		file_length_s = float(info['file_length_frames']) / 60
		remaining = file_length_s - ts
		if remaining > 0.1:
			current_event_ts = '__recording_end__'
			op('timer1').par.length = remaining
			op('timer1').par.initialize.pulse()
			op('timer1').par.start.pulse()
			print("selected_csv_exec::load_next_timer: no more events, song-end timer set for {:.2f}s".format(remaining))
		else:
			print("selected_csv_exec::load_next_timer WARNING: no upcoming events after ts", ts)
	return
