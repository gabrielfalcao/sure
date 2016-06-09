from sure import expect


def test_issue_104():
    try:
        expect("hello").to.contain("world")
    except Exception:  # just to prevent syntax error because try/else does not exist
        pass
    else:
        raise SystemExit("Oops")

    expect("hello world").to.contain("world")
