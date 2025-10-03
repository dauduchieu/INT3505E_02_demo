@echo off
echo Adding book: Clean Code
curl -s -X POST http://127.0.0.1:5000/books ^
     -H "Content-Type: application/json" ^
     -d "{\"title\": \"Clean Code\", \"author\": \"Robert C. Martin\"}"
echo.

echo Adding book: Python Basic
curl -s -X POST http://127.0.0.1:5000/books ^
     -H "Content-Type: application/json" ^
     -d "{\"title\": \"Python Basic\", \"author\": \"Author 1\"}"
echo.

echo Adding book: Service-Oriented Architecture
curl -s -X POST http://127.0.0.1:5000/books ^
     -H "Content-Type: application/json" ^
     -d "{\"title\": \"Service-Oriented Architecture\", \"author\": \"Author 2\"}"
echo.

echo Done!
pause
