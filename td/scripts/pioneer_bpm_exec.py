

def onCellChange(dat, cells, prev):

  for cell in cells:
    bpm = float(cell)
    op("/project1/ui_container/resolume_container/bpm").par.Value0 = bpm
    mod("/project1/ui_container/resolume_container/sld_resolume_controller").on_bpm_change(bpm, False, False)

  return
