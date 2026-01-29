@echo off
echo.
echo ========================================
echo   FORGET TO WIN - Quick Start
echo ========================================
echo.
echo Choose an option:
echo.
echo [1] Play Full Game
echo [2] Run Demo (View Components)
echo [3] Exit
echo.
choice /c 123 /n /m "Enter your choice (1-3): "

if errorlevel 3 goto :end
if errorlevel 2 goto :demo
if errorlevel 1 goto :game

:game
cls
python main.py
goto :end

:demo
cls
python demo.py
goto :end

:end
echo.
echo Thanks for playing!
pause
