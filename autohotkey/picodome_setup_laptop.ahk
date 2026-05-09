; open all the programs
GoSub #8


; load touchdesigner
#8::
Run %A_ProgramFiles%\Derivative\TouchDesigner\bin\TouchDesigner.exe "C:\artsync\bermuda\td\Picodome.toe"
SetTitleMatchMode 2
WinWait Picodome, , 120
if ErrorLevel
{
    MsgBox, Timed out waiting for TouchDesigner to open.
    return
}
WinActivate, Picodome
WinWaitActive, Picodome
Sleep 1000
; Send, {F1}
Return
