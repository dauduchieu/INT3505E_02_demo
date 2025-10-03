@echo off
REM Get the full list of books

curl -s http://127.0.0.1:5000/books

echo.
pause
