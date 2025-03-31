#Persistent
SetTitleMatchMode, 2  ; 允许匹配窗口标题中的部分内容

; alt+f good
!f::  ; Alt+F
jsonShowAnswer := "{""action"":""guiShowAnswer"",""version"":6}"
jsonAnswer := "{""action"":""guiAnswerCard"",""version"":6,""params"":{""ease"":3}}"

tempShow := A_Temp . "\anki_show.json"
tempAnswer := A_Temp . "\anki_answer.json"

FileDelete, %tempShow%
FileDelete, %tempAnswer%
FileAppend, %jsonShowAnswer%, %tempShow%
FileAppend, %jsonAnswer%, %tempAnswer%

RunWait, C:\Windows\System32\curl.exe -X POST -H "Content-Type: application/json" -d @"%tempShow%" http://127.0.0.1:8765,, Hide
RunWait, C:\Windows\System32\curl.exe -X POST -H "Content-Type: application/json" -d @"%tempAnswer%" http://127.0.0.1:8765,, Hide

FileDelete, %tempShow%
FileDelete, %tempAnswer%
return

!d::  ; Alt+D
jsonShowAnswer := "{""action"":""guiShowAnswer"",""version"":6}"
jsonAnswer := "{""action"":""guiAnswerCard"",""version"":6,""params"":{""ease"":1}}"

tempShow := A_Temp . "\anki_show.json"
tempAnswer := A_Temp . "\anki_answer.json"

FileDelete, %tempShow%
FileDelete, %tempAnswer%
FileAppend, %jsonShowAnswer%, %tempShow%
FileAppend, %jsonAnswer%, %tempAnswer%

RunWait, C:\Windows\System32\curl.exe -X POST -H "Content-Type: application/json" -d @"%tempShow%" http://127.0.0.1:8765,, Hide
RunWait, C:\Windows\System32\curl.exe -X POST -H "Content-Type: application/json" -d @"%tempAnswer%" http://127.0.0.1:8765,, Hide

FileDelete, %tempShow%
FileDelete, %tempAnswer%
return
