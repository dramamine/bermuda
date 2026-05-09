# me - this DAT
#
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
#
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

target_table = op('/project1/ui_container/picodome_mapper/map_triangle_segment_lengths')

def incrementUp():
  col = int(op('table_indices').par.Value1)
  row = int(op('table_indices').par.Value0)
  # print(f"incrementUp: col={col}, row={row}")
  if col == 15:
    op('table_indices').par.Value1 = 1
    op('table_indices').par.Value0 = (row % 20) + 1
  else:
    op('table_indices').par.Value1 = col + 1

def incrementDown():
  col = int(op('table_indices').par.Value1)
  row = int(op('table_indices').par.Value0)
  # print(f"incrementDown: col={col}, row={row}")
  if col == 1:
    op('table_indices').par.Value1 = 15
    op('table_indices').par.Value0 = ((row - 2) % 20) + 1
  else:
    op('table_indices').par.Value1 = col - 1

def editValue(delta):
  row = int(op('table_indices').par.Value0)
  col = int(op('table_indices').par.Value1)
  current = int(target_table[row, col])
  target_table[row, col] = current + delta

def onOffToOn(channel, sampleIndex, val, prev):
  if channel.name == 'kup':
    incrementUp()
  elif channel.name == 'kdown':
    incrementDown()
  elif channel.name == 'kright':
    editValue(1)
  elif channel.name == 'kleft':
    editValue(-1)




  return

def whileOn(channel, sampleIndex, val, prev):
  return

def onOnToOff(channel, sampleIndex, val, prev):
  return

def whileOff(channel, sampleIndex, val, prev):
  return

def onValueChange(channel, sampleIndex, val, prev):
  return
