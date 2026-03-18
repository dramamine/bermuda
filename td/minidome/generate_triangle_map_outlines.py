"""
DAT Execute DAT

me - this DAT

dat - the changed DAT
prevDAT - a simulated DAT containing previous contents

Info contains specific details on what's changed:

	rowsChanged	- list of row indices with different contents
	rowsAdded	- list of added row name indices (in dat)
	rowsRemoved	- list of removed row name indices (in prevDAT)

	colsChanged	- list of column indices with different contents
	colsAdded	- list of added column name indices (in dat)
	colsRemoved	- list of removed column name indices (in prevDAT)

	cellsChanged 	- list of cells that have changed content

	sizeChanged	- bool, true if number of rows or columns changed

Make sure the corresponding toggle is enabled in the DAT Execute DAT.
"""

import math
from typing import List, Tuple

# 72-degree rotation in radians (one fifth of a full turn)
ROTATION = 2 * math.pi / 5
CENTER_ORIGIN = 500  # rotation pivot point


def rotate_point(x: float, y: float, angle: float) -> Tuple[float, float]:
	"""
	Rotate a point (x, y) around (CENTER_ORIGIN, CENTER_ORIGIN) by the given angle in radians.

	Args:
		x: The x coordinate to rotate
		y: The y coordinate to rotate
		angle: The rotation angle in radians

	Returns:
		A tuple (x', y') of the rotated coordinates
	"""
	cos_a = math.cos(angle)
	sin_a = math.sin(angle)
	dx = x - CENTER_ORIGIN
	dy = y - CENTER_ORIGIN
	x_rot = CENTER_ORIGIN + dx * cos_a - dy * sin_a
	y_rot = CENTER_ORIGIN + dy * cos_a + dx * sin_a
	return (x_rot, y_rot)


NUM_OUTLINES = 5
OUTLINE_DISTANCES = [1.0, 0.8, 0.6, 0.4, 0.2]  # fraction of center-to-corner distance
OUTLINE_LENGTHS = [16, 13, 10, 6, 3]


def onTableChange(dat: DAT, prevDAT: DAT, info: ChangedDATInfo):
	"""
	Called when a table change occurs. For each source row, generates
	NUM_OUTLINES rows with the corner coordinate scaled to a decreasing
	percentage of the center-to-corner distance, plus lengths columns.

	Input columns:  triangle_idx, center.x, center.y, corner.x, corner.y
	Output columns: triangle_idx, center.x, center.y, corner.x, corner.y,
	                outline_idx, lengths.a, lengths.b, lengths.c

	Args:
		dat: The changed DAT
		prevDAT: The DAT containing previous contents
		info: ChangedDATInfo object with specific details on what changed
	"""
	print("table changed")
	output = op('triangle_map_table')

	num_source_rows = dat.numRows - 1
	if num_source_rows <= 0:
		return

	output.clear()
	output.appendRow([
		'triangle_idx', 'center.x', 'center.y', 'corner.x', 'corner.y',
		'outline_idx', 'lengths.a', 'lengths.b', 'lengths.c'
	])

	for row_idx in range(1, dat.numRows):
		triangle_idx = int(dat[row_idx, 'triangle_idx'].val)
		cx = float(dat[row_idx, 'center.x'].val)
		cy = float(dat[row_idx, 'center.y'].val)
		crx = float(dat[row_idx, 'corner.x'].val)
		cry = float(dat[row_idx, 'corner.y'].val)

		for outline_idx in range(NUM_OUTLINES):
			pct = OUTLINE_DISTANCES[outline_idx]
			length = OUTLINE_LENGTHS[outline_idx]

			# Scale corner toward center by the distance percentage
			adj_crx = cx + (crx - cx) * pct
			adj_cry = cy + (cry - cy) * pct

			output.appendRow([
				triangle_idx, cx, cy, adj_crx, adj_cry,
				outline_idx, length, length, length
			])

	return

# The following legacy callbacks can be used to track individual changes.
# Note that if rows or columns are deleted, sizeChange will be called instead
# of row/col/cellChange.


def onRowChange(dat: DAT, rows: List[int]):
	"""
	Called when rows change.

	Args:
		dat: The changed DAT
		rows: A list of row indices that changed
	"""
	return


def onColChange(dat: DAT, cols: List[int]):
	"""
	Called when columns change.

	Args:
		dat: The changed DAT
		cols: A list of column indices that changed
	"""
	return


def onCellChange(dat: DAT, cells: List[Cell], prev: List[str]):
	# onTableChange(dat, None, None)
	"""
	Called when cells change.

	Args:
		dat: The changed DAT
		cells: List of cells that have changed content
		prev: List of previous string contents of the changed cells
	"""
	return


def onSizeChange(dat: DAT):
	"""
	Called when the size (rows or columns) of the DAT changes.

	Args:
		dat: The changed DAT
	"""
	return
