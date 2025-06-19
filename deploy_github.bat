@echo off
echo ========================================
echo    MPPT数据分析平台 - GitHub部署脚本
echo ========================================
echo.

REM 检查是否在正确的目录
if not exist "interactive_visualizer.py" (
    echo ❌ 错误：未找到主程序文件，请确保在项目根目录运行此脚本
    pause
    exit /b 1
)

echo 📋 准备部署到GitHub...
echo.

REM 提示用户输入GitHub仓库信息
set /p GITHUB_USERNAME="请输入您的GitHub用户名: "
set /p REPO_NAME="请输入仓库名称（如 mppt-analytics）: "

echo.
echo 🔧 正在初始化Git仓库...

REM 初始化Git仓库（如果尚未初始化）
if not exist ".git" (
    git init
    echo ✅ Git仓库已初始化
) else (
    echo ℹ️  Git仓库已存在
)

echo.
echo 📦 正在添加文件到暂存区...
git add .

echo.
echo 💾 正在提交代码...
git commit -m "🎉 Initial commit: MPPT数据分析与可视化平台

✨ 功能特性:
- 📊 交互式MPPT数据可视化
- 🤖 机器学习预测（线性回归 + XGBoost）
- 📈 置信区间可视化（68%%, 95%%, 99%%）
- 🌤️ 气象数据集成分析
- 📱 响应式Web界面

🛠️ 技术栈:
- Streamlit + Pandas + NumPy
- Scikit-learn + XGBoost + Plotly
- Python 3.8+"

if %ERRORLEVEL% neq 0 (
    echo ⚠️  提交可能失败，但继续执行...
)

echo.
echo 🌿 正在设置主分支...
git branch -M main

echo.
echo 🔗 正在添加远程仓库...
set REPO_URL=https://github.com/%GITHUB_USERNAME%/%REPO_NAME%.git
echo 仓库URL: %REPO_URL%

REM 检查是否已存在远程仓库配置
git remote get-url origin >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ℹ️  远程仓库已存在，正在更新...
    git remote set-url origin %REPO_URL%
) else (
    echo ➕ 正在添加远程仓库...
    git remote add origin %REPO_URL%
)

echo.
echo 🚀 正在推送到GitHub...
echo 注意：如果提示需要认证，请使用GitHub Personal Access Token
echo.

git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================
    echo           🎉 部署成功！
    echo ========================================
    echo.
    echo 📱 您的项目已成功推送到GitHub!
    echo 🌐 仓库地址: https://github.com/%GITHUB_USERNAME%/%REPO_NAME%
    echo.
    echo 🚀 接下来您可以：
    echo   1. 访问仓库查看代码
    echo   2. 部署到Streamlit Cloud
    echo   3. 设置GitHub Pages（如果需要）
    echo.
    echo 📖 详细部署指南请查看 GITHUB_DEPLOY_GUIDE.md
    echo ========================================
) else (
    echo.
    echo ========================================
    echo           ❌ 部署失败
    echo ========================================
    echo.
    echo 可能的原因：
    echo   1. 网络连接问题
    echo   2. GitHub认证失败
    echo   3. 仓库不存在或无权限
    echo.
    echo 💡 解决方案：
    echo   1. 检查网络连接
    echo   2. 确保GitHub仓库已创建
    echo   3. 使用Personal Access Token认证
    echo   4. 查看详细错误信息
    echo.
    echo 📖 详细说明请查看 GITHUB_DEPLOY_GUIDE.md
    echo ========================================
)

echo.
pause
