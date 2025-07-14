# me - this DAT
#
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
#
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

# def onOffToOn(channel, sampleIndex, val, prev):
# 	return


# def whileOn(channel, sampleIndex, val, prev):
# 	return


# def onOnToOff(channel, sampleIndex, val, prev):
# 	return


# def whileOff(channel, sampleIndex, val, prev):
# 	return


def onValueChange(channel, sampleIndex, val, prev):
  mod("/project1/ui_container/resolume_container/sld_resolume_commands").set_dashboard_value(
    1, 3, val
  )
  return
