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
current_player = 1
# section = 0

low_mood = {
  'intro': range(2, 4),  # deprecated, now just ignoring intro
  'verse': range(4, 6),
  'bridge': range(3, 6),
  'chorus': range(7, 10),
  'outro': range(1, 4)
}

mid_mood = {
  'intro': range(1, 4),  # deprecated, now just ignoring intro
  'verse': range(7, 10),
  'bridge': range(4, 7),
  'chorus': range(9, 15),
  'outro': range(3, 6)
}

high_mood = {
  'intro': range(1, 4),  # deprecated, now just ignoring intro
  'up': range(7, 10), # deprecated, now just raises intensity
  'down': range(4, 7), # deprecated, now just lowers intensity
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
  print("pioneer sync called")
  bpm = float( op('pioneer_data')[1, 'bpm'] )
  # print("my bpm is:", bpm)
  beat = op('pioneer_data')[1, 'beat']
  # print("my beat is:", beat)
  if beat == '1':
    op("/project1/ui_container/resolume_container/bpm").par.Value0 = bpm
    mod("/project1/ui_container/resolume_container/sld_resolume_controller").on_bpm_change(bpm, True, True)
    op("/project1/ui_container/pioneer_link/trigger1").par.triggerpulse.pulse()
    print("done syncing from phrase change")


def onCellChange(dat, cells, prev):
  global mood, phrase, section

  # do any cells have '1' or '2' in them?
  if '1' in cells or '2' in cells:
    print("master_player_number changed so I'm ignoring the phase change")
    return

  for cell in cells:
    print("pioneer_exec::updated phrasee:", cell)
    next = str(cell).split('-')
    next_mood = next[0]
    next_phrase = next[1]

    if next_phrase != phrase:
      # hard transition
      if next_phrase in ['verse', 'bridge', 'chorus', 'outro']:
        op('time_since_last_change').par.start.pulse()
        # next_section = 0
        next_intensity = random.choice(moods[next_mood][next_phrase])
        mod("/project1/ui_container/resolume_container/sld_resolume_controller").choose_intensity(next_intensity)
        next_transition_time = 0 if next_phrase == 'chorus' else 2
        mod("/project1/ui_container/resolume_container/sld_resolume_controller").load_pattern_and_play(next_transition_time)
        sync()
      elif next_phrase in ['up']:
        current_intensity = mod("/project1/ui_container/resolume_container/sld_resolume_controller").get_intensity()
        print("on up: going to add 2 to intensity:", current_intensity)
        mod("/project1/ui_container/resolume_container/sld_resolume_controller").set_intensity(current_intensity + 2)
        print("intensity is now:", mod("/project1/ui_container/resolume_container/sld_resolume_controller").get_intensity())
      elif next_phrase in ['down']:
        current_intensity = mod("/project1/ui_container/resolume_container/sld_resolume_controller").get_intensity()
        print("on down: going to subtract 2 from intensity:", current_intensity)
        mod("/project1/ui_container/resolume_container/sld_resolume_controller").set_intensity(current_intensity - 2)
        print("intensity is now:", mod("/project1/ui_container/resolume_container/sld_resolume_controller").get_intensity())

    mood = next_mood
    phrase = next_phrase
  # section = next_section
  return

def onSizeChange(dat):
  return
