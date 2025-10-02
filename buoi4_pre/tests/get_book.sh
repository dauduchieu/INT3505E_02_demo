# Get a single book by ID
# Usage: ./get_book.sh <id>

if [ -z "$1" ]; then
  echo "Usage: ./get_book.sh <book_id>"
  exit 1
fi

curl -s http://127.0.0.1:5000/books/$1 | jq .
