
import math

triangle_map = op("triangle_map_table")
replicator = op("replicator1")

# --- Test pattern mode ---
# When True, generate_panel_map() writes color-chart u,v coords instead of
# world-space coords. test_source_switch should also be set to input 1.
test_mode = False

_TEST_SLOTS = 4
_TEST_IMAGE_WIDTH = 1000
_TEST_IMAGE_V = 1000  # vertical center of the test image


def _test_color_slot(idx, length):
    """Return color slot 0-3 for pixel at position idx in a segment of given length.

    Slot 0=green, 1=yellow, 2=red, 3=black.
    Mirrors from both ends: first and last pixel are green, next inner pair yellow, etc.
    """
    pos = min(idx, length - 1 - idx)
    return min(pos, 3)


def _test_uv(slot):
    """Return (u, v) at the center of the given color band in the test image."""
    band_width = _TEST_IMAGE_WIDTH / _TEST_SLOTS
    return (band_width * slot + band_width / 2, _TEST_IMAGE_V)


def generate_test_pixelmap(triangle):
    """Return (u, v) tuples using color-chart coords for every pixel in the triangle.

    Iterates sides a, b, c exactly like generate_pixelmap() but maps each pixel
    to a color band based on its position within the segment.
    """
    sides = [
        triangle["lengths"]["a"],
        triangle["lengths"]["b"],
        triangle["lengths"]["c"],
    ]
    pixels = []
    for length in sides:
        for i in range(length):
            pixels.append(_test_uv(_test_color_slot(i, length)))
    return pixels


def set_test_mode(enabled):
    """Enable or disable test pattern mode and regenerate the pixel map."""
    global test_mode
    test_mode = bool(enabled)
    # op("test_source_switch").par.index = 1 if test_mode else 0
    generate_panel_map()


def generate_pixelmap(triangle):
    """Generate pixel coordinates along the edges of a triangle.

    The triangle is defined by its center and one corner vertex.
    The other two vertices are derived by rotating the corner around the center
    by 120° and 240°. Pixels are evenly distributed along each side:
      - Side a: corner → vertex 2 (conceptually bottom, left to right)
      - Side b: vertex 2 → vertex 3 (conceptually right side, bottom to top)
      - Side c: vertex 3 → corner (conceptually left side, top to bottom)

    Returns a list of (x, y) tuples for each pixel.
    """
    cx = triangle["center"]["x"]
    cy = triangle["center"]["y"]
    corner_x = triangle["corner"]["x"]
    corner_y = triangle["corner"]["y"]

    def rotate(px, py, angle_deg):
        """Rotate point (px, py) around the triangle center by angle_deg degrees."""
        rad = math.radians(angle_deg)
        dx, dy = px - cx, py - cy
        return (
            cx + dx * math.cos(rad) - dy * math.sin(rad),
            cy + dx * math.sin(rad) + dy * math.cos(rad),
        )

    # Derive all three vertices from the given corner (clockwise winding)
    v0 = (corner_x, corner_y)
    v1 = rotate(corner_x, corner_y, -120)
    v2 = rotate(corner_x, corner_y, -240)

    # Side a: v0 → v1, side b: v1 → v2, side c: v2 → v0
    sides = [
        (v0, v1, triangle["lengths"]["a"]),
        (v1, v2, triangle["lengths"]["b"]),
        (v2, v0, triangle["lengths"]["c"]),
    ]

    pixels = []
    for start, end, num_pixels in sides:
        for i in range(num_pixels):
            # Place each pixel at the midpoint of its segment along the side
            t = (i + 0.5) / num_pixels
            x = start[0] + t * (end[0] - start[0])
            y = start[1] + t * (end[1] - start[1])
            pixels.append((x, y))

    return pixels


def generate_panel_map(source=triangle_map):
    """Read triangle definitions from the source table and build a full pixel map.

    Each row in the source table defines a triangle with columns:
      center.x, center.y, corner.x, corner.y,
      lengths.a, lengths.b, lengths.c,
      triangle_idx, outline_idx

    Pixels are written to per-panel tables at:
      pixelmap_to_universes_container{triangle_idx}/pixelmap_table
    """
    # Set replicator count to the highest triangle_idx (last row)
    num_panels = int(source[source.numRows - 1, "triangle_idx"])
    replicator.par.numreplicants = num_panels

    # Clear and initialize the allpoints table for normalized coordinates
    allpoints = op("allpoints")
    allpoints.clear()
    allpoints.appendRow(["tx", "ty", "tz"])

    # update dmx routing table
    generate_routing_table(source=triangle_map, routingtable=op("dmxout1_routingtable"))

    # Track a running index per panel
    panel_indices = {}

    for row_idx in range(1, source.numRows):  # skip header row
        tri_idx = int(source[row_idx, "triangle_idx"])

        triangle = {
            "center": {
                "x": float(source[row_idx, "center.x"]),
                "y": float(source[row_idx, "center.y"]),
            },
            "corner": {
                "x": float(source[row_idx, "corner.x"]),
                "y": float(source[row_idx, "corner.y"]),
            },
            "lengths": {
                "a": int(source[row_idx, "lengths.a"]),
                "b": int(source[row_idx, "lengths.b"]),
                "c": int(source[row_idx, "lengths.c"]),
            },
        }

        table = op(f"pixelmap_to_universes_container{tri_idx}/pixelmap_table")

        # Clear the table on first encounter of this panel
        if tri_idx not in panel_indices:
            panel_indices[tri_idx] = 0
            table.clear()
            table.appendRow(["index", "u", "v"])

        pixels = generate_test_pixelmap(triangle) if test_mode else generate_pixelmap(triangle)
        for x, y in pixels:
            table.appendRow([panel_indices[tri_idx], x, y])
            allpoints.appendRow([x / 1000, y / 1000, 0])
            panel_indices[tri_idx] += 1


def generate_routing_table(source=triangle_map, routingtable=None, universes_per_triangle=2):
    """Write DMX routing rows to the specified table DAT.

    Creates one row per universe. Channel names follow the pattern
    ``uni_{triangle_idx}_{local_universe}``. The universe column increments
    globally across all triangles.

    Args:
        source: Table DAT with triangle definitions (needs triangle_idx column).
        routingtable: The table DAT to write to. Defaults to op("dmxout1_routingtable").
        universes_per_triangle: Number of DMX universes each triangle uses.
    """
    if routingtable is None:
        routingtable = op("dmxout1_routingtable")

    # Collect unique triangle indices (preserving order)
    seen = set()
    triangle_indices = []
    for row_idx in range(1, source.numRows):
        tri_idx = int(source[row_idx, "triangle_idx"])
        if tri_idx not in seen:
            seen.add(tri_idx)
            triangle_indices.append(tri_idx)

    routingtable.clear()
    routingtable.appendRow(["channel", "net", "subnet", "universe"])

    global_universe = 1
    for tri_idx in triangle_indices:
        for local_uni in range(universes_per_triangle):
            routingtable.appendRow([
                f"uni_{tri_idx}_{local_uni}",
                0,
                0,
                global_universe,
            ])
            global_universe += 1
