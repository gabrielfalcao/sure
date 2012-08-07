## sure [1.0.0] - utility belt for automated testing in python
[![Build Status](https://secure.travis-ci.org/gabrielfalcao/sure.png)](http://travis-ci.org/gabrielfalcao/sure)

# Installing

    user@machine:~$ [sudo] pip install sure

# Fluent assertions with `it` and `this`

#### `exists()` and `should.exist()` asserts that the given object is truthy

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

#### `dont.exists()`, `doesnt.exists()` and `shouldnt.exist()` asserts that the given object is falsy

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

#### `{'a': 'collection'}.should.equal({'a': 'collection'})` does deep comparation

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

# Python compatibility


```

Python >= 2.6

```


# About sure 1.0

The assertion library is 100% inspired be the awesomeness of [should.js](https://github.com/visionmedia/should.js) which is simple, declarative and fluent.


## Authors

[Gabriel Falcão](http://github.com/gabrielfalcao) and [Lincoln Clarete](http://github.com/clarete)
