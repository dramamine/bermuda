## Bermuda - TouchDesigner Interface

This interface has a couple components:
- Audio analysis
- Pioneer DJ Link interpretation (bpm / beat sync)
- Pioneer mixer MIDI interpretation (for some gimmicks like triggering Resolume effects from mixer FX and EQ levels)
- Playlist mode for pre-sequenced tracks
- Audio controls

## Mixer Config

Connected to the DJM-900NXS2. Be sure to map this (Alt+D, or Dialogs -> MIDI Device Mapper) to device 1.

DJM-250MK2 was set up in Bermuda.120.toe and earlier. The mappings are all in `/project1/ui_container/pioneer_link/pioneer_dj_link/select1`

## Phrase Recorder

`/project1/ui_container/pioneer_link/pioneer_dj_link/phrase_change_recorder_container`

This is part of functionality to record phrase changes to CSV files.

Generally leave this disabled.

