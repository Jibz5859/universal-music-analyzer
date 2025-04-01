@echo off
title Sine Wave Plot Generator
color 0A
echo === Plot Generation Started ===
echo.

:: Verify conda exists
where conda >nul 2>&1 || (
    echo ERROR: Conda not found in PATH
    pause
    exit /b 1
)

:: Activate environment
call conda activate newproject || (
    echo ERROR: Failed to activate 'newproject' environment
    echo Available environments:
    call conda env list
    pause
    exit /b 1
)

:: Run Python script
python src\newproject\scripts\test_plot.py || (
    echo ERROR: Python script failed
    pause
    exit /b 1
)

:: Show last 3 plots (Windows compatible)
echo.
echo Last 3 plots:
for /f "skip=1 tokens=*" %%i in ('dir /O-D /B "%CD%\outputs\sine_wave_*.png"') do (
    echo %%i
    set /a count+=1
    if !count! geq 3 goto :done
)
:done

echo.
echo Press any key to exit...
pause >nul