@echo off

REM Kill the Python script by its window title
taskkill /FI "WINDOWTITLE eq quiz.py" /F

REM Play the video file using Windows Media Player and wait for it to finish
start /wait wmplayer "quiz.mp4"

REM Start the Python script
start python quiz.py
