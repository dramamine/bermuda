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


def onTableChange(dat: DAT, prevDAT: DAT, info: ChangedDATInfo):
	"""
	Called when a table change occurs. For each source row, generates four
	additional rows rotated by 72, 144, 216, and 288 degrees around
	(CENTER_ORIGIN, CENTER_ORIGIN).

	Expects columns: triangle_idx, center.x, center.y, corner.x, corner.y

	Args:
		dat: The changed DAT
		prevDAT: The DAT containing previous contents
		info: ChangedDATInfo object with specific details on what changed
	"""
	print("table changed")
	output = op('triangle_map_table2')  # the DAT this script is attached to

	# Read all source rows (skip header row at index 0)
	num_source_rows = dat.numRows - 1
	if num_source_rows <= 0:
		return

	# Start with a copy of the header
	output.clear()
	output.appendRow([dat[0, c].val for c in range(dat.numCols)])

	# Build all rows (original + rotated) into a list
	rows = []
	for row_idx in range(1, dat.numRows):
		raw = dat[row_idx, 'triangle_idx'].val
		if not raw or not raw.strip():
			continue
		try:
			triangle_idx = int(raw)
		except ValueError:
			continue

		cx = float(dat[row_idx, 'center.x'].val)
		cy = 1000 - float(dat[row_idx, 'center.y'].val)
		crx = float(dat[row_idx, 'corner.x'].val)
		cry = 1000 - float(dat[row_idx, 'corner.y'].val)

		# Original row (rotation 0)
		rows.append([triangle_idx, round(cx), round(cy), round(crx), round(cry)])

		# 4 rotated copies (72°, 144°, 216°, 288°)
		for i in range(1, 5):
			angle = ROTATION * i
			new_cx, new_cy = rotate_point(cx, cy, angle)
			new_crx, new_cry = rotate_point(crx, cry, angle)
			new_idx = triangle_idx + num_source_rows * i
			rows.append([new_idx, round(new_cx), round(new_cy), round(new_crx), round(new_cry)])

	# Sort by triangle_idx and write to output
	rows.sort(key=lambda r: r[0])
	for row in rows:
		output.appendRow(row)

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
