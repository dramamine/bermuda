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
import random


mood = 'low'
phrase = 'intro'
section = 0

low_mood = {
  'intro': range(2, 4),
  'verse': range(4, 6),
  'bridge': range(3, 6),
  'chorus': range(7, 10),
  'outro': range(1, 4)
}

mid_mood = {
  'intro': range(1, 4),
  'verse': range(7, 10),
  'bridge': range(4, 7),
  'chorus': range(9, 15),
  'outro': range(3, 6)
}

high_mood = {
  'intro': range(1, 4),
  'up': range(7, 10),
  'down': range(4, 7),
  'chorus': range(9, 15),
  'outro': range(3, 6)
}

moods = {
  'low': low_mood,
  'mid': mid_mood,
  'high': high_mood
}

def onTableChange(dat):
  return

def onRowChange(dat, rows):
  for row in rows:
    print("row change:", row)
  return

def onColChange(dat, cols):
  return

def sync():
  bpm = float( op('pioneer_data')[1, 'bpm'] )
  # print("my bpm is:", bpm)
  beat = op('pioneer_data')[1, 'beat']
  # print("my beat is:", beat)
  if beat == '1':
    op("/project1/ui_container/resolume_container/bpm").par.Value0 = bpm
    mod("/project1/ui_container/resolume_container/sld_resolume_controller").on_bpm_change(bpm, True, True)
    print("done syncing from phrase change")


def onCellChange(dat, cells, prev):
  global mood, phrase, section
  for cell in cells:
    print("updated phrasee:", cell)
    next = str(cell).split('-')
    next_mood = next[0]
    next_phrase = next[1]
    next_section = int(next[2]) if len(next) >= 3 else 0
    # needs starting or has completed
    #enough_time_has_passed = op('time_since_last_change').fraction >= 1.0 or op('time_since_last_change').fraction == 0.0
    if next_phrase != phrase:
      op('time_since_last_change').par.start.pulse()
      next_intensity = random.choice(moods[next_mood][next_phrase])
      # print("pioneer_exec: will use intensity:", next_intensity,
      #       "from:", moods[next_mood][next_phrase])
      mod("/project1/ui_container/resolume_container/sld_resolume_controller").choose_intensity(next_intensity)
      next_transition_time = 0 if next_phrase == 'chorus' else 2
      mod("/project1/ui_container/resolume_container/sld_resolume_controller").load_pattern_and_play(next_transition_time)
      sync()

    mood = next_mood
    phrase = next_phrase
    section = next_section
  return

def onSizeChange(dat):
  return
