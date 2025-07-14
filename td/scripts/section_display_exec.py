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
import math


def onTableChange(dat):
	val = float(dat[1, 'timer_fraction'].val)
	fourth_a = math.floor(val / 0.25)
	op('table1')[0, 0] = fourth_a + 1
	op('filein1').par.file = f'./images/beat{fourth_a + 1}.png'

	remainder = val - (fourth_a * 0.25)
	fourth_b = math.floor(remainder / (0.0625 / 2)) % 4
	op('table1')[0, 1] = fourth_b + 1
	op('filein2').par.file = f'./images/beat{fourth_b + 1}.png'

	# remainder -= fourth_b * 0.0625
	# fourth_c = math.floor(remainder / 0.03125)
	# op('filein3').par.file = f'./images/beat{fourth_c + 1}.png'

	section = int(dat[1, 'section'].val)
	op('filein4').par.file = f'./images/beat{section+1}.png'

	return


def onRowChange(dat, rows):
	return


def onColChange(dat, cols):
	return


def onCellChange(dat, cells, prev):
	return


def onSizeChange(dat):
	return
