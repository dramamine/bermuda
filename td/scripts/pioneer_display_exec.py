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


def onTableChange(dat):
	val = int(dat[1, 0].val)
	op('filein1').par.file = f'./images/beat{val}.png'

	val = int(dat[2, 0].val)
	op('filein2').par.file = f'./images/beat{val}.png'
	return


def onRowChange(dat, rows):
	return

def onColChange(dat, cols):
	return

def onCellChange(dat, cells, prev):
	return

def onSizeChange(dat):
	return
