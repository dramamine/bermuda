# me - this DAT
# par - the Par object that has changed
# val - the current value
# prev - the previous value
#
# Make sure the corresponding toggle is enabled in the Parameter Execute DAT.

def onValueChange(par, prev):
	# use par.eval() to get current value
	print("audio_toggle_exec::toggle updated:", par.eval())

	if (par.eval() == True):
		# turn off internal playlist audio
		op('/project1/ui_container/playlist_container/playlist_toggle_exec').par.Value0 = False
		op('audiodevin1').bypass = 0
	else:
		op('audiodevin1').bypass = 1

	return

# Called at end of frame with complete list of individual parameter changes.
# The changes are a list of named tuples, where each tuple is (Par, previous value)


def onValuesChanged(changes):
	for c in changes:
		# use par.eval() to get current value
		par = c.par
		prev = c.prev
	return


def onPulse(par):
	return


def onExpressionChange(par, val, prev):
	return


def onExportChange(par, val, prev):
	return


def onEnableChange(par, val, prev):
	return


def onModeChange(par, val, prev):
	return
