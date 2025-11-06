// GET /books/1

pm.test("Book found", () => pm.response.to.have.status(200));

pm.test("Book has title & author", () => {
    const json = pm.response.json();
    pm.expect(json).to.have.property("title");
    pm.expect(json).to.have.property("author");
});

pm.test("Check book id", function () {
    const jsonData = pm.response.json();
    pm.expect(jsonData.id).to.eql(1);
});
