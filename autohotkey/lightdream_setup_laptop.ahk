; open all the programs
GoSub #7
GoSub #8
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
Run %A_ProgramFiles%\Derivative\TouchDesigner\bin\TouchDesigner.exe "C:\artsync\lightdream-scripts\td\Bermuda.toe"
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





; load USC
; #9::
; Run C:\git\lightdream-scripts\usc\usc-game.exe -notitle
; WinWait USC-Game, , 60
; if ErrorLevel
; {
;     MsgBox, Timed out waiting for USC to open.
;     return
; }
; WinActivate, USC-Game
; WinWaitActive, USC-Game
; Return

; ; run python script
; #0::
; dir    := "C:\git\lightdream-artnet"
; script  = %dir%\main.py
; F3::Run, %ComSpec% /k python "%script%"