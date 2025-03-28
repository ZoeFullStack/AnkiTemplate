#Persistent
SetTitleMatchMode, 2  ; 允许匹配窗口标题中的部分内容
F2::  ; Press F2 to show the answer and select "Again"
; Step 1: Show the answer
jsonShowAnswer := "{""action"":""guiShowAnswer"",""version"":6}"
tempFileShow := A_Temp . "\anki_showanswer.json"
FileDelete, %tempFileShow%  ; Delete old JSON file
FileAppend, %jsonShowAnswer%, %tempFileShow%

cmdShow := "C:\Windows\System32\curl.exe -X POST -H ""Content-Type: application/json"" -d @""" tempFileShow """ http://127.0.0.1:8765 > " A_Temp "\response_show.txt"
RunWait, %cmdShow%, , UseErrorLevel

; Step 2: Answer the card (select "Again")
jsonAnswer := "{""action"":""guiAnswerCard"",""version"":6,""params"":{""ease"":1}}"
tempFileAnswer := A_Temp . "\anki_answer.json"
FileDelete, %tempFileAnswer%  ; Delete old JSON file
FileAppend, %jsonAnswer%, %tempFileAnswer%

cmdAnswer := "C:\Windows\System32\curl.exe -X POST -H ""Content-Type: application/json"" -d @""" tempFileAnswer """ http://127.0.0.1:8765 > " A_Temp "\response_answer.txt"
RunWait, %cmdAnswer%, , UseErrorLevel

; Step 3: Read and log responses (optional)
FileRead, responseShow, %A_Temp%\response_show.txt
FileRead, responseAnswer, %A_Temp%\response_answer.txt

; Optional: Write responses to a log file (if needed)
logFile := A_Temp . "\anki_log.txt"
FileAppend, Show answer response: %responseShow%`nAnswer card response: %responseAnswer%`n, %logFile%

; Clean up temporary files
FileDelete, %A_Temp%\response_show.txt
FileDelete, %A_Temp%\response_answer.txt
FileDelete, %tempFileShow%
FileDelete, %tempFileAnswer%
return