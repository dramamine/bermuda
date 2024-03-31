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

is_ordered = False
current_idx = 1
def onTableChange(dat):
  global is_ordered, current_idx
  print("playlist_script::table has changed.")
  if (str(dat[1,0]).startswith("01 ")):
    print("playlist_script::ordered playlist")
    is_ordered = True
    current_idx = 1
    pickFirstTrack()
  else:
    print("playlist_script::random playlist")
    is_ordered = False
    pickRandomTrack()
  return


def onRowChange(dat, rows):
  return


def onColChange(dat, cols):
  return


def onCellChange(dat, cells, prev):
  return


def onSizeChange(dat):
  return

def pickFirstTrack():
  rows = op('playlist_folder_musics').numRows
  if rows <= 1:
    return

  chosen_value = op('playlist_folder_musics')[1, 0]
  op('music_dropdown').par.Value0 = chosen_value
  return

def pickNextTrack():
  global current_idx

  rows = op('playlist_folder_musics').numRows
  if rows <= 1:
    return

  current_idx += 1
  if current_idx >= rows:
    current_idx = 1

  chosen_value = op('playlist_folder_musics')[current_idx, 0]
  op('music_dropdown').par.Value0 = chosen_value
  return

def pickRandomTrack():
  rows = op('playlist_folder_musics').numRows
  if rows <= 1:
    return

  selected = int(
    op('/project1/timecode_xp/playlist_container/music_dropdown_value')['menuIndex']) + 1
  options = list(filter(lambda x: x != selected, range(1, rows)))
  chosen_idx = random.choice(options)
  chosen_value = op('playlist_folder_musics')[chosen_idx, 0]
  print(rows, selected, options, chosen_idx, chosen_value)
  op('music_dropdown').par.Value0 = chosen_value
  return

def next_track():
  # TODO do I need to confirm toggles?
  if is_ordered:
    pickNextTrack()
  else:
    pickRandomTrack()
  return
