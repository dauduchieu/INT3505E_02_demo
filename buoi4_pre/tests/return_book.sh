#!/bin/bash
# Return a book by ID
# Usage: ./return_book.sh <id>

if [ -z "$1" ]; then
  echo "Usage: ./return_book.sh <book_id>"
  exit 1
fi

curl -s -X PUT http://127.0.0.1:5000/books/$1/return | jq .
