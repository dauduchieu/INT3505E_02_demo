# JWT authentication and authorization
# code implemented at rest/v6_authen_author.py
# test jwt:
- [POST] http://127.0.0.1:5000/login
    - Request:
        - username: user
        - password: 123
    - Response:
        - token
        - copy token to next step test
- [GET] http://127.0.0.1:5000/books (require authentication)
    - no authorization token: err: 401 Unauthorized
    - add copied token to authorization token: 200 Success
- [POST] http://127.0.0.1:5000/books (require admin authorization)
    - no authorization token: err: 401 Unauthorized
    - add copied token to authorization token: 403 Forbidden
    - Re-login with username "admin", password "123" to get admin token
    - add copied admin token to authorization token: 201 Success
