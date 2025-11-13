## **Case Study: Payment API v1 → v2**

### 1. API v1

**Endpoints:**

* `POST /api/v1/payments` → tạo thanh toán

  ```json
  {
    "amount": 100.0,
    "currency": "USD",
    "user_id": 1
  }
  ```

* `GET /api/v1/payments/<id>` → lấy thông tin thanh toán

**Vấn đề / Hạn chế:**

* Không hỗ trợ nhiều loại phương thức thanh toán (chỉ mặc định “card”)
* Không có `status` chi tiết (chỉ trả `success: true/false`)
* Không chuẩn hóa mã lỗi

---

### 2. API v2 (breaking change)

**Endpoints:**

* `POST /api/v2/payments`

  ```json
  {
    "amount": 100.0,
    "currency": "USD",
    "user_id": 1,
    "payment_method": "card",
    "description": "Order #123"
  }
  ```

* `GET /api/v2/payments/<id>`

  ```json
  {
    "id": 1,
    "amount": 100.0,
    "currency": "USD",
    "user_id": 1,
    "payment_method": "card",
    "status": "completed",
    "description": "Order #123"
  }
  ```

**Cải tiến:**

* Hỗ trợ nhiều phương thức thanh toán
* Trả `status` chi tiết (`pending`, `completed`, `failed`)
* Có thể thêm `metadata` nếu cần

---

### 3. Chiến lược versioning

**URL versioning**:

* V1: `/api/v1/payments`
* V2: `/api/v2/payments`

**Deprecation plan cho v1**:

1. **Thông báo sớm:**

   * Header `Warning: 299 - "API v1 will be deprecated on 2025-12-31. Please migrate to v2"`

2. **Grace period:**

   * 6 tháng chạy song song v1 & v2

3. **Disable v1:**

   * Ngừng hỗ trợ sau ngày 2025-12-31

---

### 4. Ví dụ header deprecation

```http
GET /api/v1/payments HTTP/1.1
Authorization: Bearer <token>

HTTP/1.1 200 OK
Content-Type: application/json
Warning: 299 - "API v1 will be deprecated on 2025-12-31. Please migrate to v2"
[
    { "id": 1, "amount": 100.0, "currency": "USD", "user_id": 1 }
]
```