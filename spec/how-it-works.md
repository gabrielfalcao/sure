# How sure works

The class `sure.AssertionBuilder` creates objects capable of doing
assertions. The AssertionBuilder simply arranges a vast set of
possible assertions that are composed by a `source` object and a
`destination` object.

Every assertion, even implicitly if implicitly like in `(2 < 3).should.be.true`, is doing a source/destination matching.


## Chainability

Some specific assertion methods are chainable, it can be useful for short assertions like:

```python
PERSON = {
  "name": "John",
  "facebook_info": {
    "token": "abcd"
  }
}

PERSON.should.have.key("facebook_info").being.a(dict)
```

# Monkey-patching

Lincoln Clarete has written the module [`sure/magic.py`] which I simply added to sure. The most exciting part of the story is that Lincoln exposed the code with a super clean API, it's called [forbidden fruit](http://clarete.github.io/forbiddenfruit/)

## Why CPython-only ?

Sure uses the [ctypes](http://docs.python.org/library/ctypes) module
to break in python protections against monkey patching.

Although ctypes might also be available in other implementations such
as [Jython](http://www.jython.org/), only the CPython provide
[`ctypes.pythonapi`](http://docs.python.org/library/ctypes#loading-shared-libraries)
the features required by sure.
