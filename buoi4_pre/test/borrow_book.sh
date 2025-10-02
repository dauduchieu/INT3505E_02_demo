# POST /borrows
# {
#   "book_id": 1
# }

curl -X POST http://127.0.0.1:5000/books \
     -H "Content-Type: application/json" \
     -d '{"book_id": 1}'
