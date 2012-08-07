## sure `1.0.0alpha` - utility belt for automated testing in python
[![Build Status](https://secure.travis-ci.org/gabrielfalcao/sure.png)](http://travis-ci.org/gabrielfalcao/sure)

```python
from sure import version

version.should.be.equal('1.0.0alpha')
```

# Installing

    user@machine:~$ [sudo] pip install sure

# Static assertions with `it`, `this`, `those` and `these`

#### `exists()` and `should.exist()` asserts that the given object is truthy

```python
from sure import it, this, these, those

assert it.should.exist(True)
assert it.exists(object())

assert this.should.exist(True)
assert this.exists(object())

assert it.should.exist(True)
assert it.exists(object())

assert this.should.exists(True)
assert this.should.exists(object())

bugs = []
assert those.shouldnt.exist(bugs)

users = []
assert these.shouldnt.exist(users)

```

#### `dont.exists()`, `doesnt.exists()` and `shouldnt.exist()` asserts that the given object is falsy

```python
from sure import it, this, these, those

assert it.dont.exist({})
assert it.dont.exist([])
assert it.dont.exist('')
assert it.dont.exist(False)
assert it.dont.exist(None)

assert these.dont.exist({})
assert these.dont.exist([])
assert these.dont.exist('')
assert these.dont.exist(False)
assert these.dont.exist(None)

assert it.doesnt.exist({})
assert it.doesnt.exist([])
assert it.doesnt.exist('')
assert it.doesnt.exist(False)
assert it.doesnt.exist(None)

assert those.doesnt.exist({})
assert those.doesnt.exist([])
assert those.doesnt.exist('')
assert those.doesnt.exist(False)
assert those.doesnt.exist(None)

assert this.dont.exist({})
assert this.dont.exist([])
assert this.dont.exist('')
assert this.dont.exist(False)
assert this.dont.exist(None)

assert this.doesnt.exist({})
assert this.doesnt.exist([])
assert this.doesnt.exist('')
assert this.doesnt.exist(False)
assert this.doesnt.exist(None)

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

#### `should.be.ok` and `shouldnt.be.ok`

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

# Fluent assertions

> available only on cpython (no support for Jython, IronPython, PyPy, etc)

Mind-blowing easy and fluent assertions.

#### `(number).should.equal(number)`

```python
import sure

(4).should.be.equal(2 + 2)
(7.5).should.eql(3.5 + 4)
(2).should.equal(8 / 4)

(3).shouldnt.be.equal(10 / 3)
```

#### `{'a': 'collection'}.should.equal({'a': 'collection'})` does deep comparison

```python
{'foo': 'bar'}.should.equal({'foo': 'bar'})
{'foo': 'bar'}.should.eql({'foo': 'bar'})


```

#### `"A string".lower().should.equal("a string")` also works

```python
"Awesome ASSERTIONS".lower().split().should.equal(['awesome', 'assertions'])
```

#### `{iterable}.should.be.empty` applies to any iterable of length 0

```python

[].should.be.empty;
{}.should.be.empty;
set().should.be.empty;
"".should.be.empty;
().should.be.empty
range(0).should.be.empty;

# negate with:

[1, 2, 3].shouldnt.be.empty;
"Lincoln de Sousa".shouldnt.be.empty;
```


#### `{number}.should.be.within(0, 10)` asserts inclusive numeric range:

```python
(1).should.be.within(0, 2)
(5).should.be.within(10)

# negate with:

(1).shouldnt.be.within(5, 6)
```

#### `{member}.should.be.within({iterable})` asserts that a member is part of the iterable:

```python
"g".should.be.within("gabriel")
'name'.should.be.within({'name': 'Gabriel'})
'Lincoln'.should.be.within(['Lincoln', 'Gabriel'])

# negate with:

'Bug'.shouldnt.be.within(['Sure 1.0'])
```

#### lists, tuples
# Python compatibility

## Those are the python versions that support the assertions above `([CPython](http://en.wikipedia.org/wiki/CPython))`


```

Python ~= 2.6 (CPython)
Python ~= 2.7 (CPython)

```

## Not supported:

```

Jython

PyPy

IronPython

UnladenSwallow

StacklessPython

...
```

## Why CPython-only ?

Sure has a slick algorithm that makes use of the
[ctypes](http://docs.python.org/library/ctypes), and although it is
also available in other implementations such as
[Jython](http://www.jython.org/) does have the `ctypes` module, only
the CPython provides
[`ctypes.pythonapi`](http://docs.python.org/library/ctypes#loading-shared-libraries),
required by sure.

### Holy guacamole, how did you implement that feature ?

Differently of [ruby](http://www.ruby-lang.org) python doesn't have
[open classes](http://blog.aizatto.com/2007/06/01/ruby-and-open-classes/),
but [Lincoln de Sousa](https://github.com/clarete/) came out with a
super [sick code](https://github.com/gabrielfalcao/sure/blob/master/sure/magic.py) that uses the ctypes module to create a pointer to the
`__dict__` of builtin types.

Yes, it is dangerous, non-pythonic and should not be used in production code.

Although `sure` is here to be used __ONLY__ in test code, therefore it
should be running in __ONLY__ possible environments: your local
machine or your continuous-integration server.

# About sure 1.0

The assertion library is 100% inspired be the awesomeness of [should.js](https://github.com/visionmedia/should.js) which is simple, declarative and fluent.

# Old API

Sure still provides to all the assertions from v0.10 up, you can [find the old documentation here](https://github.com/gabrielfalcao/sure/blob/master/OLD_API.md)

## Authors

[Gabriel Falcão](http://github.com/gabrielfalcao) and [Lincoln Clarete](http://github.com/clarete)
