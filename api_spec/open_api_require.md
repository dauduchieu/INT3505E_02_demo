1. Top-level metadata: Nhóm các trường đầu tài liệu OpenAPI mô tả “khung” của API
2. Paths: các đường dẫn API chứa methods cùng mô tả, tham số, requestBody và responses tương ứng
3. Components: “Kho dùng chung” để tái sử dụng các định nghĩa như schemas, parameters, ...
4. Schemas: Các mô hình dữ liệu để mô tả cấu trúc request/response body
5. Parameters: Các tham số ngoài body xuất hiện ở in: path | query | header | cookie

**Example**
openapi: 3.0.4
info:
  title: Sample API
  description: Optional multiline or single-line description in [CommonMark](http://commonmark.org/help/) or HTML.
  version: 0.1.9

servers:
  - url: http://api.example.com/v1
    description: Optional server description, e.g. Main (production) server
  - url: http://staging-api.example.com
    description: Optional server description, e.g. Internal staging server for testing

paths:
  /users:
    get:
      summary: Returns a list of users.
      description: Optional extended description in CommonMark or HTML.
      responses:
        "200": # status code
          description: A JSON array of user names
          content:
            application/json:
              schema:
                type: array
                items:
                  type: string
