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
	alignment_map = op('alignment_map')
	lookup_name = op('triangle_idx')[1, 0].val

	if alignment_map is None:
		print("No alignment_map operator found")
		return

	matched_row_idx = None
	for r in range(1, alignment_map.numRows):
		if alignment_map[r, 'name'].val == lookup_name:
			matched_row_idx = r
			break

	if matched_row_idx is None:
		print("No alignment_map row found for name:", lookup_name)
		return

	row_cells = alignment_map.row(matched_row_idx)
	ip = alignment_map[matched_row_idx, 'ip'].val
	name = alignment_map[matched_row_idx, 'name'].val
	alignment_idx = alignment_map[matched_row_idx, 'alignment_idx'].val

	op('value_selector').par.Value0 = alignment_idx
	# print("Dropdown interaction: active row {} -> name={} ip={} alignment_idx={}".format(
	# 	matched_row_idx, name, ip, alignment_idx
	# ))

	return


def onRowChange(dat, rows):
	return


def onColChange(dat, cols):
	return


def onCellChange(dat, cells, prev):
	return


def onSizeChange(dat):
	return
