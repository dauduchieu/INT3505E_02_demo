// Author: Bearer {{token}}

pm.test("Status 200", () => pm.response.to.have.status(200))

pm.test("Response time < 500ms", () => pm.expect(pm.response.responseTime).to.be.below(500))

pm.test("Response has results array", () => {
    let json = pm.response.json()
    pm.expect(json.results).to.be.an("array")
})
