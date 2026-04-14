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

# If True, always play tracks in order (never random)
force_ordered = True

current_idx = 1
def onTableChange(dat):

  global is_ordered, current_idx
  # print("playlist_music_exec::table has changed.")
  if force_ordered or str(dat[1,0]).startswith("01 "):
    print("playlist_music_exec::ordered playlist (forced)" if force_ordered else "playlist_music_exec::ordered playlist")
    current_idx = 1
    pickFirstTrack()
  else:
    print("playlist_music_exec::random playlist")
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
  current_name = str(op('/project1/ui_container/playlist_manager/playlist_container/selected_music')[1, 0])
  musics = op('playlist_folder_musics')
  rows = musics.numRows

  # find current track by exact name match (skip header row 0)
  current_row = None
  for i in range(1, rows):
    if str(musics[i, 0]) == current_name:
      current_row = i
      break

  if current_row is None:
    print("pickNextTrack: could not find current track '{}', starting from first.".format(current_name))
    next_row = 1
  else:
    next_row = current_row + 1
    if next_row >= rows:
      print("pickNextTrack: reached end of playlist, wrapping to first track.")
      next_row = 1

  next_value = musics[next_row, 0]
  print("pickNextTrack: playing row {} '{}'".format(next_row, next_value))
  op('music_dropdown').par.Value0 = next_value
  return

def pickRandomTrack():
  # print("playlist_music_exec::pickRandomTrack")
  rows = op('playlist_folder_musics').numRows
  if rows <= 1:
    return

  selected = int(
    op('music_dropdown_value')['menuIndex']) + 1
  options = list(filter(lambda x: x != selected, range(1, rows)))
  chosen_idx = random.choice(options)
  chosen_value = op('playlist_folder_musics')[chosen_idx, 0]
  # print(rows, selected, options, chosen_idx, chosen_value)
  op('music_dropdown').par.Value0 = chosen_value
  return

def next_track():
  # print("next_track called...")
  # first, clear out any timer stuff
  op('/project1/ui_container/playlist_manager/timer1').par.initialize.pulse()
  op("/project1/ui_container/resolume_container/section_timer").par.initialize.pulse()
  # print("next_track called...")
  # TODO do I need to confirm toggles?
  if force_ordered or str(op('playlist_folder_musics')[1, 0]).startswith("01 "):
    pickNextTrack()
  else:
    print("picking random track...")
    pickRandomTrack()
  return
