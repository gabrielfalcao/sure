from sure import expect

def raise_err(foobar):
    raise ValueError()

def test_issue_48():
    expect(raise_err).when.called_with('asdf').should.throw(ValueError)
