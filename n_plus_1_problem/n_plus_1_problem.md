# N+1 problem with 2 objects
## Get all authors of all books
- Problem:
```python
authors = Author.query.all()  # 1 query

for author in authors:
    print(author.name)
    books = Book.query.filter_by(author_id=author.id).all()  # N queries
    print(len(books))

# N + 1 queries
```
- Solution: Join
```python
from sqlalchemy.orm import joinedload

authors = Author.query.options(joinedload(Author.books)).all()

# ORM join and process in 1 query
```

# N+1 problem with 3 objects
## Get all publishers of all books of all authors
- Problem:
```python
authors = Author.query.all()  # 1 query

for author in authors:
    books = Book.query.filter_by(author_id=author.id).all()  # N queries
    for book in books:
        publisher = Publisher.query.get(book.publisher_id)  # M queries

# 1 + N + M queries
```
- Solution: Join
```python
from sqlalchemy.orm import joinedload

authors = (
    Author.query
    .options(
        joinedload(Author.books)
        .joinedload(Book.publisher)
    )
    .all()
)

# ORM join and process in 1 query
```
```sql
SELECT * 
FROM authors
LEFT JOIN books ON authors.id = books.author_id
LEFT JOIN publishers ON books.publisher_id = publishers.id;
```

