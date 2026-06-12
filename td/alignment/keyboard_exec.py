# me - this DAT
#
# channel - the Channel object which has changed
# sampleIndex - the index of the changed sample
# val - the numeric value of the changed sample
# prev - the previous sample value
#
# Make sure the corresponding toggle is enabled in the CHOP Execute DAT.

def _find_alignment_row(alignment_map, lookup_name):
  for r in range(1, alignment_map.numRows):
    if alignment_map[r, 'name'].val == lookup_name:
      return r
  return None


def incrementRow(delta):
  alignment_map = op('alignment_map')
  triangle_idx = op('triangle_idx')

  if alignment_map is None or triangle_idx is None:
    print('alignment_map or triangle_idx not found')
    return None

  lookup_name = triangle_idx[1, 0].val

  current_row = _find_alignment_row(alignment_map, lookup_name)
  if current_row is None:
    print('No alignment_map row found for name:', lookup_name)
    return None

  first_row = 1
  last_row = alignment_map.numRows - 1
  new_row = max(first_row, min(last_row, current_row + delta))

  if new_row == current_row:
    return {
      'changed': False,
      'name': lookup_name,
      'row': current_row,
    }

  new_name = alignment_map[new_row, 'name'].val

  dropdown_triangle = op('dropdown_triangle')
  if dropdown_triangle is None:
    print('dropdown_triangle not found')
    return None

  dropdown_triangle.par.Value0 = new_name
  return {
    'changed': True,
    'name': new_name,
    'row': new_row,
  }


def updateAlignmentValue(delta):
  alignment_options = op('alignment_options')
  value_selector = op('value_selector')

  if alignment_options is None or value_selector is None:
    print('alignment_options or value_selector not found')
    return None

  min_value = 0
  max_value = alignment_options.numRows - 1
  current = int(value_selector.par.Value0)
  new_value = max(min_value, min(max_value, current + delta))
  value_selector.par.Value0 = new_value
  return {
    'old': current,
    'new': new_value,
    'max': max_value,
  }

def onOffToOn(channel, sampleIndex, val, prev):
  if channel.name == 'kup':
    incrementRow(1)
  elif channel.name == 'kdown':
    incrementRow(-1)
  elif channel.name == 'kleft':
    updateAlignmentValue(-1)
  elif channel.name == 'kright':
    updateAlignmentValue(1)

  return

def whileOn(channel, sampleIndex, val, prev):
  return

def onOnToOff(channel, sampleIndex, val, prev):
  return

def whileOff(channel, sampleIndex, val, prev):
  return

def onValueChange(channel, sampleIndex, val, prev):
  return
