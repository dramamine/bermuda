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
current_event_ts = '0.000'


def onRowChange(dat, rows):
	print("selected_csv_exec::row has changed.", rows)

	is_toggle_on = op('./playlist_toggle').par.Value0.eval()
	if not is_toggle_on:
		return

	print(dat[1, 1])
	path = str(dat[1, 1])
	mp3_path = path.replace("csv", "mp3")
	op('audiofilein1').par.file = mp3_path
	play_song()

	return


def play_song():
	op('timecode1').par.init.pulse()
	op('timecode1').par.start.pulse()
	load_next_timer(use_zero=True)
	pass


def reset_timecode():
	op('timecode1').par.init.pulse()
	op('timer1').par.initialize.pulse()
	return


def do_current_action():
	global current_event_ts
	print("current action")
	for i in range(1, op('text1').numRows):
		event_ts = op('text1')[i, 0]
		if (current_event_ts != event_ts):
			continue

		current_action = op('text1')[i, 1]
		value1 = op('text1')[i, 2]
		value2 = op('text1')[i, 3]
		if current_action == "set_intensity":
			mod("/project1/ui_container/resolume_container/sld_resolume_controller").choose_intensity(int(value1))
			mod("/project1/ui_container/resolume_container/sld_resolume_controller").activate()
		elif current_action == "set_transition_type":
			# @TODO make sure this doesn't conflict with set_intensity, otherwise might need to sandwich it between choose_intensity & activate
			mod("/project1/ui_container/resolume_container/sld_resolume_controller").set_transition_type("TODO", "TODO")
		elif current_action == "set_bpm":
			mod("/project1/ui_container/resolume_container/sld_resolume_controller").update_bpm(int(value1))

	return


def load_next_timer(use_zero=False):
	global current_event_ts
	# read timestamp
	ts = 0 if use_zero else op('timecode1')['total_seconds']
	print("ts:", ts)

	# get next upcoming event
	for i in range(1, op('text1').numRows):
		event_ts = float(op('text1')[i, 0])
		if event_ts > ts + 0.005:
			print("next event:", event_ts)
			current_event_ts = op('text1')[i, 0]

			# set timer
			op('timer1').par.length = event_ts - ts
			op('timer1').par.initialize.pulse()
			op('timer1').par.start.pulse()
			# @TODO
			break
	return
