; open all the programs
; GoSub #7
; GoSub #8
; GoSub #9


; load resolume, turn on Advanced Output
#7::
Run, %A_ProgramFiles%\Resolume Arena 6\Arena.exe
WinWait Resolume Arena, , 120
if ErrorLevel
{
    MsgBox, Timed out waiting for Resolume to open.
    return
}

WinWait Resolume Arena - Bermuda, , 120
if ErrorLevel
{
    MsgBox, Timed out waiting for Resolume with our comp loaded.
    return
}
Sleep 2500
WinActivate, Resolume Arena
WinWaitActive, Resolume Arena
Send, +^a
Sleep 3000
WinMinimize, Advanced Output
Return

; load touchdesigner
#8::
Run %A_ProgramFiles%\Derivative\TouchDesigner.2023.11510\bin\TouchDesigner.exe "E:\git\lightdream-scripts\td\Bermuda.toe"
SetTitleMatchMode 2
WinWait Bermuda, , 120
if ErrorLevel
{
    MsgBox, Timed out waiting for TouchDesigner to open.
    return
}
WinActivate, Bermuda
WinWaitActive, Bermuda
Sleep 1000
; Send, {F1}
Return

; load Beat Link Trigger
#9::
Run, %A_ProgramFiles%\Deep Symmetry\Beat Link Trigger\Beat Link Trigger.exe
WinWait Beat Link Triggers, , 15
WinWaitActive, Beat Link Triggers
if ErrorLevel
{
    MsgBox, Timed out waiting for Beat Link Trigger to open.
    return
}
SetTitleMatchMode 2
WinWait Beat Link Show, , 15
if ErrorLevel
{
    MsgBox, "The show doesn't seem to be open. In the following dialog, please navigate to C:/artsync/lightdream-scripts/bermuda-show.bls and open it."
    WinWaitActive, Beat Link Triggers
    Send, ^o
    return
}
Return

;

; Navigate the file open dialog and open C:/artsync/lightdream-scripts/bermuda-show.bls


; WinActivate, rekordbox
; WinWaitActive, rekordbox
; MsgBox, rekordbox is open
; set window size to 1000x1000
; WinMove, rekordbox,, 0, 0, 1000, 1000
