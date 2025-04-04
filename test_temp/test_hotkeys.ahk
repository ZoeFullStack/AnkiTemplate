#Persistent
SetTitleMatchMode, 2  ; 允许匹配窗口标题中的部分内容

; Alt+F 提交“好”答案
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

; Alt+D 提交“再次”答案
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

; Alt+S 刷新当前卡片正面,重新播放语音
!s::  ; Alt+S
jsonShowQuestion := "{""action"":""guiShowQuestion"",""version"":6}"

tempShowQuestion := A_Temp . "\anki_show_question.json"

FileDelete, %tempShowQuestion%
FileAppend, %jsonShowQuestion%, %tempShowQuestion%

; 调用 guiShowQuestion 刷新正面内容
RunWait, C:\Windows\System32\curl.exe -X POST -H "Content-Type: application/json" -d @"%tempShowQuestion%" http://127.0.0.1:8765,, Hide

FileDelete, %tempShowQuestion%
return

; Alt+A 显示答案
!a::  ; Alt+A
jsonShowAnswer := "{""action"":""guiShowAnswer"",""version"":6}"

tempShow := A_Temp . "\anki_show.json"

FileDelete, %tempShow%
FileAppend, %jsonShowAnswer%, %tempShow%

; 调用 guiShowAnswer 显示答案
RunWait, C:\Windows\System32\curl.exe -X POST -H "Content-Type: application/json" -d @"%tempShow%" http://127.0.0.1:8765,, Hide

FileDelete, %tempShow%
return
