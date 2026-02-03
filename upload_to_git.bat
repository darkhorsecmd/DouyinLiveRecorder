@echo off
chcp 65001
echo ==========================================
echo       DouyinLiveRecorder Git 上传助手
echo ==========================================

echo [1/5] 检查 Git 环境...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Git 工具！
    echo 请访问 https://git-scm.com/download/win 下载并安装 Git。
    echo 安装后请重新运行此脚本。
    pause
    exit /b
)

echo [2/5] 初始化/检查 Git 仓库...
if not exist .git (
    git init
    echo 仓库初始化完成。
) else (
    echo 检测到已有 Git 仓库。
)

echo [3/5] 添加文件更改...
git add .

echo [4/5] 提交更改...
git commit -m "feat: add Feishu push notification support"

echo.
echo [5/5] 推送到远程仓库
echo ------------------------------------------
echo 请输入你的远程仓库地址 (例如 https://github.com/yourname/repo.git)
echo 如果只想保存在本地，请直接按回车跳过。
echo ------------------------------------------
set /p remote_url="远程仓库地址: "

if "%remote_url%"=="" (
    echo.
    echo 已跳过推送步骤。代码已提交到本地仓库。
) else (
    echo.
    echo 正在配置远程仓库 origin...
    git remote remove origin >nul 2>&1
    git remote add origin %remote_url%
    
    echo.
    echo 正在推送代码...
    git push -u origin main
    if %errorlevel% neq 0 (
        echo.
        echo 推送失败。尝试推送到 master 分支...
        git push -u origin master
    )
)

echo.
echo ==========================================
echo                 操作完成
echo ==========================================
pause
