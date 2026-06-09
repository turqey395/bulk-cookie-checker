@echo off
echo Installing dependencies...
pip install requests ttkbootstrap
echo.
echo Starting Netflix Cookie Checker...
python cookie_checker.py
pause
