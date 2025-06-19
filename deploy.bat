@echo off
echo ======================================
echo    MPPT Platform - GitHub Deployment
echo ======================================
echo.

REM 检查Git是否安装
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

REM 检查是否已初始化Git
if not exist ".git" (
    echo Initializing Git repository...
    git init
)

echo Adding files to Git...
git add .

echo Committing changes...
git commit -m "Initial commit: MPPT数据分析与可视化平台"

REM 设置远程仓库
set /p repo_url="请输入你的GitHub仓库URL: "
git remote remove origin 2>nul
git remote add origin %repo_url%

echo Pushing to GitHub...
git branch -M main
git push -u origin main

echo.
echo ======================================
echo    部署完成！
echo ======================================
echo.
echo 现在你可以:
echo 1. 访问你的GitHub仓库查看代码
echo 2. 在Streamlit Cloud (https://share.streamlit.io) 部署应用
echo 3. 连接GitHub仓库并选择 interactive_visualizer.py 作为入口文件
echo.
pause
