// Auth: Bearer {{token}} // after login with role admin
// Body: { "title": "New Book", "author": "Me" }

pm.test("Created", () => pm.response.to.have.status(201));

let json = pm.response.json();
pm.environment.set("new_book_id", json.id);

pm.test("Response contains new id", () => pm.expect(json.id).to.exist);
