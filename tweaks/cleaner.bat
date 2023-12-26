del /s /f /q C:\windows\temp\*.* 
rd /s /q C:\windows\temp 
md c:\windows\temp 
del /s /f /q C:\Windows\Prefetch
del /s /f /q %temp%\*.* 
rd /s /q %temp% 
cls 
timeout 1 >nul 
cls 
timeout 3 >nul 
md %temp% 
del /q /f /s C:\Temp\*.* 
del /q /f /s C:\Windows\Prefetch\*.* 
del /q /f /s C:\*.log 
del /q /f /s C:\*.bak 
del /q /f /s C:\*.gid 