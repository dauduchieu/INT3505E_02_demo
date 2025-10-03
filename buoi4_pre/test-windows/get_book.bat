@echo off
REM Get a single book by ID
REM Usage: get_book.bat <book_id>

if "%~1"=="" (
    echo Usage: get_book.bat ^<book_id^>
    exit /b 1
)

curl -s http://127.0.0.1:5000/books/%1

echo.
pause
