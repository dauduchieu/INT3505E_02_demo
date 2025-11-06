// body: { "username": "admin", "password": "123" }

pm.test("Authorization is success", function() {
    pm.response.to.have.status(200)
})

const json = pm.response.json()
pm.test("Token exist", () => {
    pm.expect(json.token).to.exist
})

pm.environment.set("token", json.token)
