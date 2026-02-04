@echo off
chcp 65001 > nul
echo -----------------------------------------------------
echo ^|                DouyinLiveRecorder Web Console      ^|
echo -----------------------------------------------------
echo.
echo [INFO] 正在启动 Web 控制台...
echo [INFO] 请勿关闭此窗口
echo [INFO] 启动成功后，请在浏览器访问: http://localhost:8000
echo.

python web_backend.py

pause
