@echo off
echo ========================================
echo     MPPT项目 - 部署前状态检查
echo ========================================
echo.

set ERROR_COUNT=0

echo 🔍 正在检查项目文件...
echo.

REM 检查主程序文件
if exist "interactive_visualizer.py" (
    echo ✅ 主程序文件: interactive_visualizer.py
) else (
    echo ❌ 缺少主程序文件: interactive_visualizer.py
    set /a ERROR_COUNT+=1
)

REM 检查依赖文件
if exist "requirements.txt" (
    echo ✅ 依赖文件: requirements.txt
) else (
    echo ❌ 缺少依赖文件: requirements.txt
    set /a ERROR_COUNT+=1
)

REM 检查README
if exist "README.md" (
    echo ✅ 说明文件: README.md
) else (
    echo ⚠️  建议添加: README.md
)

REM 检查部署相关文件
if exist ".gitignore" (
    echo ✅ Git忽略文件: .gitignore
) else (
    echo ⚠️  建议添加: .gitignore
)

if exist "LICENSE" (
    echo ✅ 许可证文件: LICENSE
) else (
    echo ℹ️  可选文件: LICENSE
)

REM 检查配置文件
if exist "config.json" (
    echo ✅ 配置文件: config.json
) else (
    echo ℹ️  配置文件: config.json （如果需要）
)

REM 检查Streamlit配置
if exist ".streamlit\config.toml" (
    echo ✅ Streamlit配置: .streamlit\config.toml
) else (
    echo ℹ️ Streamlit配置: .streamlit\config.toml （用于云端部署）
)

REM 检查Docker文件
if exist "Dockerfile" (
    echo ✅ Docker配置: Dockerfile
) else (
    echo ℹ️  Docker配置: Dockerfile （用于容器化部署）
)

echo.
echo 📊 正在检查数据文件...

REM 检查数据目录
if exist "十五舍" (
    echo ✅ 数据目录: 十五舍/
    if exist "十五舍\filtered" (
        echo ✅ 过滤数据: 十五舍\filtered\
    )
) else (
    echo ⚠️  数据目录: 十五舍/ （部署时可能需要示例数据）
)

if exist "专教" (
    echo ✅ 数据目录: 专教/
)

echo.
echo 🐍 正在检查Python环境...

REM 检查Python
python --version >NUL 2>&1
if %ERRORLEVEL% equ 0 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo ✅ Python版本: %%i
) else (
    echo ❌ Python未安装或不在PATH中
    set /a ERROR_COUNT+=1
)

REM 检查pip
pip --version >NUL 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ pip已安装
) else (
    echo ❌ pip未安装
    set /a ERROR_COUNT+=1
)

echo.
echo 📦 正在检查关键依赖...

REM 检查Streamlit
python -c "import streamlit" >NUL 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Streamlit已安装
) else (
    echo ⚠️  Streamlit未安装 - 运行: pip install streamlit
)

REM 检查pandas
python -c "import pandas" >NUL 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Pandas已安装
) else (
    echo ⚠️  Pandas未安装 - 运行: pip install pandas
)

echo.
echo 🔧 正在检查Git配置...

REM 检查Git
git --version >NUL 2>&1
if %ERRORLEVEL% equ 0 (
    for /f "tokens=*" %%i in ('git --version 2^>^&1') do echo ✅ Git版本: %%i
    
    REM 检查Git用户配置
    for /f "tokens=*" %%i in ('git config --global user.name 2^>^&1') do (
        if not "%%i"=="" (
            echo ✅ Git用户名: %%i
        ) else (
            echo ⚠️  未配置Git用户名 - 运行: git config --global user.name "Your Name"
        )
    )
    
    for /f "tokens=*" %%i in ('git config --global user.email 2^>^&1') do (
        if not "%%i"=="" (
            echo ✅ Git邮箱: %%i
        ) else (
            echo ⚠️  未配置Git邮箱 - 运行: git config --global user.email "your@email.com"
        )
    )
) else (
    echo ❌ Git未安装
    set /a ERROR_COUNT+=1
)

echo.
echo ========================================

if %ERROR_COUNT% equ 0 (
    echo           🎉 检查完成
    echo ========================================
    echo.
    echo ✅ 所有必需文件都存在
    echo ✅ 环境配置正常
    echo.
    echo 🚀 您可以开始部署了！
    echo.
    echo 💡 建议的部署步骤：
    echo   1. 运行: deploy_github.bat （一键GitHub部署）
    echo   2. 或查看: GITHUB_DEPLOY_GUIDE.md （详细指南）
    echo   3. 部署到Streamlit Cloud获得在线访问
    echo.
) else (
    echo           ⚠️  发现问题
    echo ========================================
    echo.
    echo 发现 %ERROR_COUNT% 个关键问题需要解决
    echo.
    echo 📋 请按照上述提示解决问题后再部署
    echo 📖 详细说明请查看 GITHUB_DEPLOY_GUIDE.md
    echo.
)

echo ========================================
pause
