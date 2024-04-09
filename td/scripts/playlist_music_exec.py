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

current_idx = 1
def onTableChange(dat):
  global is_ordered, current_idx
  print("playlist_music_exec::table has changed.")
  if (str(dat[1,0]).startswith("01 ")):
    print("playlist_music_exec::ordered playlist")
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
  # read current value
  current_track = int(str(
      op('/project1/ui_container/playlist_container/playlist_container/selected_music')[1, 0])[:2])

  rows = op('playlist_folder_musics').numRows
  if rows <= current_track:
    # @TODO better test the last tracks
    print("pickNextTrack: rows <= current_track so im setting current_track to 1.")
    current_track = 1
    return

  op('music_dropdown').par.Value0 = current_track

  # global current_idx
  # print("playlist_music_exec::pickRandomTrack, current index:", current_idx)


  # current_idx += 1
  # if current_idx >= rows:
  #   current_idx = 1

  # chosen_value = op('playlist_folder_musics')[current_idx, 0]
  # op('music_dropdown').par.Value0 = chosen_value
  # print("playlist_music_exec::pickRandomTrack dropdown value is now:", chosen_value)
  return

def pickRandomTrack():
  print("playlist_music_exec::pickRandomTrack")
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
  print("next_track called...")
  # TODO do I need to confirm toggles?
  if (str(op('playlist_folder_musics')[1, 0])).startswith("01 "):
    pickNextTrack()
  else:
    pickRandomTrack()
  return
