@echo off
title MPPT数据采集与可视化系统

:main
cls
echo.
echo ===============================================
echo    MPPT数据采集与可视化系统
echo ===============================================
echo.
echo 请选择要执行的操作:
echo.
echo [1] 安装依赖包
echo [2] 启动数据采集器  
echo [3] 执行一次数据采集
echo [4] 启动可视化界面
echo [5] 启动Jupyter Notebook
echo [6] 查看系统状态
echo [7] 创建配置文件模板
echo [0] 退出
echo.
set /p choice=请输入选项 (0-7): 

if "%choice%"=="1" (
    cls
    echo.
    echo 正在安装依赖包...
    python launcher.py install
    echo.
    pause
    goto main
)

if "%choice%"=="2" (
    cls
    echo.
    echo 启动数据采集器...
    echo 按 Ctrl+C 停止采集
    python launcher.py collector
    echo.
    pause
    goto main
)

if "%choice%"=="3" (
    cls
    echo.
    echo 执行一次数据采集...
    python launcher.py collector --once
    echo.
    pause
    goto main
)

if "%choice%"=="4" (
    cls
    echo.
    echo 启动可视化界面...
    echo 浏览器将自动打开
    python launcher.py visualizer
    echo.
    pause
    goto main
)

if "%choice%"=="5" (
    cls
    echo.
    echo 启动Jupyter Notebook...
    echo 浏览器将自动打开
    python launcher.py jupyter
    echo.
    pause
    goto main
)

if "%choice%"=="6" (
    cls
    echo.
    echo 查看系统状态...
    python launcher.py status
    echo.
    pause
    goto main
)

if "%choice%"=="7" (
    cls
    echo.
    echo 创建配置文件模板...
    python launcher.py config
    echo.
    pause
    goto main
)

if "%choice%"=="0" (
    cls
    echo.
    echo 感谢使用MPPT数据采集与可视化系统！
    echo.
    timeout /t 2 >nul
    exit /b 0
)

echo.
echo 无效选项，请重新选择
timeout /t 2 >nul
goto main
