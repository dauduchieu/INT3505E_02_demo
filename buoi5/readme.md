# Pagination:
- Offset-based pagination
- Page-based pagination (*)
- Cursor-based pagination

## (*): page-based pagination implemented at /rest/v5_paging.py
## Test pagination:
- [GET] http://localhost:5000/books?page=1&limit=2
    - 2 books per page, get page 1
- [GET] http://localhost:5000/books?page=2&limit=3
    - 3 books per page, get page 2
- [GET] http://localhost:5000/books
    - default: page=1, limit=2
