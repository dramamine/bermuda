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
		print("playlist_recorder_exec::toggled on")
		print("  Resolume recorder settings expected:")
		print("    Start: Immediately")
		print("    After Recording: Do Nothing")
		print("    Preset: ProRes 422 Normal Quality")
		print("    Stop: Manual")
		scripts.use_video_recorder = True
	else:
		print("playlist_recorder_exec::toggled off")
		scripts.use_video_recorder = False
	return
