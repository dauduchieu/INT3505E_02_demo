# POST /books
# {
#   "title": "Clean Code",
#   "author": "Robert C. Martin"
# }

curl -X POST http://127.0.0.1:5000/books \
     -H "Content-Type: application/json" \
     -d '{"title": "Clean Code", "author": "Robert C. Martin"}'

curl -X POST http://127.0.0.1:5000/books \
     -H "Content-Type: application/json" \
     -d '{"title": "Python Basic", "author": "Author 1"}'

curl -X POST http://127.0.0.1:5000/books \
     -H "Content-Type: application/json" \
     -d '{"title": "Service-Oriented Achitechture", "author": "Author 2"}'
