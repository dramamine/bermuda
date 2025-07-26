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


# def onTableChange(dat):
# 	# See if table row 1 has a column named 'phraseType'
# 	print(dat)
# 	if dat.row(1).col('phraseType') is not None:
# 		# If it does, set the value of that column in row 1 to 'newValue'
# 		dat.row(0).col(0).val = dat.row(1).col('phraseType')
# 	return
import os
import csv


def onRowChange(dat, rows):
  if not 1 in rows:
    return

  prev_phrase = op('../last_phrase_type')[1,0]
  curr_phrase = dat[1, 'phraseType']

  # TODO FIXME might want to handle cases where the track has changed but the phrase hasn't
  if prev_phrase == curr_phrase:
    return

  folder = os.path.join('playlists', str(op('playlist_field')[0,1]))
  filename = dat[1, 'trackArtist'] + ' - ' + dat[1, 'trackTitle'] + '.csv'
  timestamp = float(int(dat[1, 'trackTimeReached']) / 1000)

  # does file exist? if not, create
  if not os.path.exists(os.path.join(folder, filename)):
      with open(os.path.join(folder, filename), 'w', newline='') as f:
          writer = csv.writer(f)
          # write header
          writer.writerow(['timestamp', 'action', 'value1', 'value2', 'value3'])
          # start and set bpm
          writer.writerow([timestamp, 'start'])
          writer.writerow([timestamp, 'set_bpm', float(dat[1, 'trackBpm'])])


  action = 'phrase_change'
  value1 = curr_phrase

  with open(os.path.join(folder, filename), 'a', newline='') as f:
      writer = csv.writer(f)
      writer.writerow([timestamp, action, value1])

  return

