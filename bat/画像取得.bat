pause

SET LogFilePath="%~dp0\�摜�擾.log"

echo �J�n�@%DATE% %TIME% >> %LogFilePath%

type �R�}���h.txt | %windir%\System32\cmd.exe "/K" C:\Users\XXX\Anaconda3\Scripts\activate.bat C:\Users\XXX\Anaconda3

echo �I���@%DATE% %TIME% >> %LogFilePath%

pause
