@echo off
chcp 65001 >nul 2>&1
title MPPT System

:main
cls
echo.
echo ===============================================
echo    MPPT Data Collection and Visualization
echo ===============================================
echo.
echo Select an option:
echo.
echo [1] Install Dependencies
echo [2] Start Data Collector
echo [3] Run One-time Collection
echo [4] Start Visualization Interface
echo [5] Start Jupyter Notebook
echo [6] Check System Status
echo [7] Create Configuration Template
echo [0] Exit
echo.
set /p "choice=Enter option (0-7): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto collector
if "%choice%"=="3" goto collect_once
if "%choice%"=="4" goto visualizer
if "%choice%"=="5" goto jupyter
if "%choice%"=="6" goto status
if "%choice%"=="7" goto config
if "%choice%"=="0" goto exit

echo.
echo Invalid option, please try again.
timeout /t 2 >nul
goto main

:install
cls
echo.
echo Installing dependencies...
python launcher.py install
echo.
pause
goto main

:collector
cls
echo.
echo Starting data collector...
echo Press Ctrl+C to stop
python launcher.py collector
echo.
pause
goto main

:collect_once
cls
echo.
echo Running one-time collection...
python launcher.py collector --once
echo.
pause
goto main

:visualizer
cls
echo.
echo Starting visualization interface...
echo Browser will open automatically
python launcher.py visualizer
echo.
pause
goto main

:jupyter
cls
echo.
echo Starting Jupyter Notebook...
echo Browser will open automatically
python launcher.py jupyter
echo.
pause
goto main

:status
cls
echo.
echo Checking system status...
python launcher.py status
echo.
pause
goto main

:config
cls
echo.
echo Creating configuration template...
python launcher.py config
echo.
pause
goto main

:exit
cls
echo.
echo Thank you for using MPPT System!
echo.
timeout /t 2 >nul
exit /b 0
echo.
pause
goto menu

:exit
cls
echo.
echo 感谢使用MPPT数据采集与可视化系统！
echo.
pause
exit
