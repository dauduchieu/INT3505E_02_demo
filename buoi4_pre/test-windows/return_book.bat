@echo off
REM Return a book by ID
REM Usage: return_book.bat <book_id>

if "%~1"=="" (
    echo Usage: return_book.bat ^<book_id^>
    exit /b 1
)

curl -s -X PUT http://127.0.0.1:5000/books/%1/return

echo.
pause
