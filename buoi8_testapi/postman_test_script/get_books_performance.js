// Author: Bearer {{token}}

pm.test("Status 200", () => pm.response.to.have.status(200));

pm.test("Response time < 300ms", () => {
  pm.expect(pm.response.responseTime).to.be.below(300);
});