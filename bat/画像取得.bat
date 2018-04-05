pause

SET LogFilePath="%~dp0\画像取得.log"

echo 開始　%DATE% %TIME% >> %LogFilePath%

type コマンド.txt | %windir%\System32\cmd.exe "/K" C:\Users\XXX\Anaconda3\Scripts\activate.bat C:\Users\XXX\Anaconda3

echo 終了　%DATE% %TIME% >> %LogFilePath%

pause
