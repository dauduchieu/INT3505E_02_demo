@echo off
REM Borrow a book by ID
REM Usage: borrow_book.bat <book_id>

if "%~1"=="" (
    echo Usage: borrow_book.bat ^<book_id^>
    exit /b 1
)

curl -s -X PUT http://127.0.0.1:5000/books/%1/borrow

echo.
pause
