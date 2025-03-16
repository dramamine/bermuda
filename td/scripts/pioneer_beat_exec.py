

def onCellChange(dat, cells, prev):
  global mood, phrase, section
  # Getting phrase data? don't need to do this
  if op('pioneer_receiving_state').par.Value0:
    return

  if op('time_since_last_change').fraction < 1.0:
    return

  for cell in cells:
    # print("cell change!:", int(cell))
    if int(cell) == 1:
      print("beat 1 syncing")
      mod("pioneer_exec").sync()
      op('time_since_last_change').par.start.pulse()

  return
