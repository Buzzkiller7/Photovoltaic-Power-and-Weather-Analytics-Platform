@echo off
echo ======================================
echo    MPPT Data Analytics and Visualization Platform
echo    Enterprise Data Analytics Dashboard
echo ======================================
echo.
echo Starting the visualization platform...
echo.

cd /d "%~dp0"

REM 检查Python环境
python --version
if %errorlevel% neq 0 (
    echo Error: could not find Python environment. 
    pause
    exit /b 1
)

REM 检查依赖包
echo Checking dependencies...
python -c "import streamlit, pandas, plotly, numpy" 2>nul
if %errorlevel% neq 0 (
    echo Warning: relevant packages may not be installed.
    echo Trying to install...
    pip install streamlit pandas plotly numpy openpyxl
)

echo.
echo Starting the visualization platform...
echo Please visit the displayed URL in your browser
echo.

streamlit run interactive_visualizer.py --server.port 8503 --server.headless false

pause
