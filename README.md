## sure [1.0.0] - utility belt for automated testing in python
[![Build Status](https://secure.travis-ci.org/gabrielfalcao/sure.png)](http://travis-ci.org/gabrielfalcao/sure)

# Features

## Test runner with chronometer and coverage reports

_Sure_ provides you with a test runner that gives you full control
over the process to the granularity of a single test case.

You can write your tests anywhere, _sure_ will find, run, count up the
duration and allow running every test case, in the end you get
acquainted with the statistics of your python codebase: what parts
have test coverage, where you should refactor or add coverage.

It also runs [flake8](http://pypi.python.org/pypi/flake8/) against
your test code and blame you when your tests are too complex

Ahh yes, you can also run only a given subset of test cases, force
slow tests to fail.

## "that": Slick, fluent assertions

_Sure_ comes with `that`, an inteligent class that provides an
hassle-less interface for writing various types of assertions.


## Behavior-driven development

Differently of [lettuce](http://lettuce.it), _Sure_ leverages pure
python test code to work and look like behavior-driven stories while
allowing you to

* Track dependencies during steps
* Share a per-test case context of states
* Test coverage and all the other candies that comes with _Sure_'s test runner

## Non-pythonic API, intentionally

_Sure_ comes with the idea that test code is somehow different of
production code in the sense that some PEP8 and PEP20 rules can be
broken as long as for the sake of writting cleaner, simpler,
maintainable and easily understood automated tests.

### _Sure_ is implicit

You will find assertions that can have totally different behaviors
depending on the kind of objects they are comparing.


# Extras

## Test python snippets within markdown code
Do you like markdown for writting the documentation of your
application?

_Sure_ will read github-flavored markdown, look for python code and
run as tests.

In fact all the examples in this readme file are part of _Sure_'s own
test suite.

# Installing

    user@machine:~$ [sudo] pip install sure

# Fluent assertions with `it` and `this`

## `exists()` and `should.exist` asserts that the given object is truthy

```python
from sure import it, this

assert it.exists(True)
assert it.exists(object())

assert this.exists(True)
assert this.exists(object())

assert it.should.exist(True)
assert it.should.exists(object())

assert this.should.exists(True)
assert this.should.exists(object())
```

## `dont.exists()`, `doesnt.exists()` and `shouldnt.exist()` asserts that the given object is falsy

```python
from sure import it, this

assert it.dont.exists({})
assert it.dont.exists([])
assert it.dont.exists('')
assert it.dont.exists(False)
assert it.dont.exists(None)

assert it.doesnt.exists({})
assert it.doesnt.exists([])
assert it.doesnt.exists('')
assert it.doesnt.exists(False)
assert it.doesnt.exists(None)

assert this.dont.exists({})
assert this.dont.exists([])
assert this.dont.exists('')
assert this.dont.exists(False)
assert this.dont.exists(None)

assert this.doesnt.exists({})
assert this.doesnt.exists([])
assert this.doesnt.exists('')
assert this.doesnt.exists(False)
assert this.doesnt.exists(None)

assert it.shouldnt.exist({})
assert it.shouldnt.exist([])
assert it.shouldnt.exist('')
assert it.shouldnt.exist(False)
assert it.shouldnt.exist(None)

assert this.shouldnt.exist({})
assert this.shouldnt.exist([])
assert this.shouldnt.exist('')
assert this.shouldnt.exist(False)
assert this.shouldnt.exist(None)
```

## `be.ok`

Assert truthfulness:

```python
from sure import this

assert this(True).should.be.ok
assert this('truthy tring').should.be.ok
assert this({'truthy': 'dictionary'}).should.be.ok
```

And negate truthfulness:

```python

from sure import this

assert this(False).shouldnt.be.ok
assert this('').shouldnt.be.ok
assert this({}).shouldnt.be.ok
```

# Python compatibility

```

Python >= 2.6

```


# About sure 1.0

The assertion library is 100% inspired be the awesomeness of [should.js](https://github.com/visionmedia/should.js) which is simple, declarative and fluent.
