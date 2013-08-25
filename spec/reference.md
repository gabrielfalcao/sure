# Equality

## (number).should.equal(number)

```python
import sure

(4).should.be.equal(2 + 2)
(7.5).should.eql(3.5 + 4)
(2).should.equal(8 / 4)

(3).shouldnt.be.equal(5)
```

## {'a': 'collection'}.should.equal({'a': 'collection'}) does deep comparison

```python
{'foo': 'bar'}.should.equal({'foo': 'bar'})
{'foo': 'bar'}.should.eql({'foo': 'bar'})
{'foo': 'bar'}.must.be.equal({'foo': 'bar'})

```

## "A string".lower().should.equal("a string") also works

```python
"Awesome ASSERTIONS".lower().split().should.equal(['awesome', 'assertions'])
```

# Similarity

## should.look_like and should_not.look_like

```python

"""

THIS IS MY loose string
""".should.look_like('this is my loose string')

"""this one is different""".should_not.look_like('this is my loose string')
```

# Iterables

## should.contain and should_not.contain

`expect(collection).to.contain(item)` is a shorthand to `expect(item).to.be.within(collection)`

```python
"My bucket of text".should.contain('bucket')

"goosfraba".should_not.contain('anger')

[1,2,3].should.contain(2)
```

## should.match and should_not.match matches regular expression

You can also use the modifiers:

* [`re.DEBUG`](http://docs.python.org/2/library/re.html#re.DEBUG)
* [`re.I` and `re.IGNORECASE`](http://docs.python.org/2/library/re.html#re.IGNORECASE)
* [`re.M` and `re.MULTILINE`](http://docs.python.org/2/library/re.html#re.MULTILINE)
* [`re.S` and `re.DOTALL`](http://docs.python.org/2/library/re.html#re.DOTALL)
* [`re.U` and `re.UNICODE`](http://docs.python.org/2/library/re.html#re.UNICODE)
* [`re.X` and `re.VERBOSE`](http://docs.python.org/2/library/re.html#re.VERBOSE)

```python
import re

"SOME STRING".should.match(r'some \w+', re.I)

"FOO BAR CHUCK NORRIS".should_not.match(r'some \w+', re.M)
```


## {iterable}.should.be.empty applies to any iterable of length 0

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
"Lincoln de Sousa".should_not.be.empty;

```


## {number}.should.be.within(0, 10) asserts inclusive numeric range:

```python
(1).should.be.within(0, 2)
(5).should.be.within(10)

# negate with:

(1).shouldnt.be.within(5, 6)
```

## {member}.should.be.within({iterable}) asserts that a member is part of the iterable:

```python
"g".should.be.within("gabriel")
'name'.should.be.within({'name': 'Gabriel'})
'Lincoln'.should.be.within(['Lincoln', 'Gabriel'])

# negate with:

'Bug'.shouldnt.be.within(['Sure 1.0'])
'Bug'.should_not.be.within(['Sure 1.0'])

```

## should.be.none and should_not.be.none

Assert whether an object is or not `None`:

```python

value = None
value.should.be.none
None.should.be.none

"".should_not.be.none
(not None).should_not.be.none

```

## should.be.ok and shouldnt.be.ok

Assert truthfulness:

```python
from sure import this

True.should.be.ok
'truthy string'.should.be.ok
{'truthy': 'dictionary'}.should.be.ok
```

And negate truthfulness:

```python

from sure import this

False.shouldnt.be.ok
''.should_not.be.ok
{}.shouldnot.be.ok
```

## Assert existence of properties and their values

```python

class Basket(object):
    fruits = ["apple", "banana"]


basket1 = Basket()

basket1.should.have.property("fruits")
```

### .have.property().being allows chaining up

If the programmer calls `have.property()` it returns an assertion
builder of the property if it exists, so that you can chain up
assertions for the property value itself.

```python

class Basket(object):
    fruits = ["apple", "banana"]

basket2 = Basket()
basket2.should.have.property("fruits").being.equal(["apple", "banana"])
basket2.should.have.property("fruits").with_value.equal(["apple", "banana"])
basket2.should.have.property("fruits").with_value.being.equal(["apple", "banana"])
```


## Assert existence of keys and its values

```python
basket3 = dict(fruits=["apple", "banana"])
basket3.should.have.key("fruits")
```

### .have.key().being allows chaining up

If the programmer calls `have.key()` it returns an assertion
builder of the key if it exists, so that you can chain up
assertions for the dictionary key value itself.


```python

person = dict(name=None)

person.should.have.key("name").being.none
person.should.have.key("name").being.equal(None)
```

## Assert the length of objects with {iterable}.should.have.length_of(N)

```python

[3, 4].should.have.length_of(2)

"Python".should.have.length_of(6)

{'john': 'person'}.should_not.have.length_of(2)
```

## Assert the magnitude of objects with {X}.should.be.greater_than(Y) and {Y}.should.be.lower_than(X) as well as {X}.should.be.greater_than_or_equal_to(Y) and {Y}.should.be.lower_than_or_equal_to(X)

```python
(5).should.be.greater_than(4)
(5).should_not.be.greater_than(10)
(1).should.be.lower_than(2)
(1).should_not.be.lower_than(0)

(5).should.be.greater_than_or_equal_to(4)
(5).should_not.be.greater_than_or_equal_to(10)
(1).should.be.lower_than_or_equal_to(2)
(1).should_not.be.lower_than_or_equal_to(0)
```

## callable.when.called_with(arg1, kwarg1=2).should.throw(Exception)

You can use this feature to assert that a callable raises an
exception:

```python
import sure
from sure.six import PY3

if PY3:
    range.when.called_with(10, step=20).should.throw(TypeError, "range() does not take keyword arguments")
    range.when.called_with("chuck norris").should.throw(TypeError, "'str' object cannot be interpreted as an integer")
else:
    range.when.called_with(10, step="20").should.throw(TypeError, "range() takes no keyword arguments")
    range.when.called_with(b"chuck norris").should.throw("range() integer end argument expected, got str.")
range.when.called_with("chuck norris").should.throw(TypeError)
range.when.called_with(10).should_not.throw(TypeError)
```

## function.when.called_with(arg1, kwarg1=2).should.return_value(value)

This is a shorthand for testing that a callable returns the expected
result

```python
import sure

list.when.called_with([0, 1]).should.return_value([0, 1])
```

this is the same as

```
value = range(2)
value.should.equal([0, 1])
```

there are no differences between those 2 possibilities, use at will

## instance.should.be.a('typename') and instance.should.be.an('typename')

this takes a type name and checks if the class matches that name

```python
import sure

{}.should.be.a('dict')
(5).should.be.an('int')

# also works with paths to modules

range(10).should.be.a('collections.Iterable')
```

## instance.should.be.a(type) and instance.should.be.an(type)

this takes the class (type) itself and checks if the object is an instance of it

```python
import sure
from sure.six import PY3

if PY3:
    u"".should.be.an(str)
else:
    u"".should.be.an(unicode)
[].should.be.a(list)
```

## instance.should.be.above(num) and instance.should.be.below(num)

assert the instance value above and below `num`

```python
import sure

(10).should.be.below(11)
(10).should.be.above(9)
(10).should_not.be.above(11)
(10).should_not.be.below(9)
```


# Static assertions with it, this, those and these

Whether you don't like the `object.should` syntax or you are simply
not running CPython, sure still allows you to use any of the
assertions above, all you need to do is wrap the object that is being
compared in one of the following options: `it`, `this`, `those` and
`these`.

## Too long, don't read

### All those possibilities below work just as the same

```python
from sure import it, this, those, these

(10).should.be.equal(5 + 5)

this(10).should.be.equal(5 + 5)

it(10).should.be.equal(5 + 5)

these(10).should.be.equal(5 + 5)

those(10).should.be.equal(5 + 5)
```

### Also if you prefer using the assert keyword in your tests just go ahead an do it!

```python
from sure import it, this, those, these, expect

assert (10).should.be.equal(5 + 5)

assert this(10).should.be.equal(5 + 5)

assert it(10).should.be.equal(5 + 5)

assert these(10).should.be.equal(5 + 5)

assert those(10).should.be.equal(5 + 5)

expect(10).to.be.equal(5 + 5)
expect(10).to.not_be.equal(8)
```

## (lambda: None).should.be.callable

Test if something is or not callable

```python
import sure

range.should.be.callable
(lambda: None).should.be.callable;
(123).should_not.be.callable
```

### A note about the assert keyword

_you can use or not the_ `assert` _keyword, sure internally already
raises an appropriate_ `AssertionError` _with an assertion message so
that you don't have to specify your own, but you can still use_
`assert` _if you find it more semantic_

Example:

```python
import sure

"Name".lower().should.equal('name')

# or you can also use

assert "Name".lower().should.equal('name')

# or still

from sure import this

assert this("Name".lower()).should.equal('name')

# also without the assert

this("Name".lower()).should.equal('name')

```

Any of the examples above will raise their own `AssertionError` with a
meaningful error message.

# Synonyms

Sure provides you with a lot of synonyms so that you can pick the ones
that makes more sense for your tests.

Note that the examples below are merely illustrative, they work not
only with numbers but with any of the assertions you read early in
this documentation.

## Positive synonyms

```python

(2 + 2).should.be.equal(4)
(2 + 2).must.be.equal(4)
(2 + 2).does.equals(4)
(2 + 2).do.equals(4)
```

## Negative synonyms

```python
from sure import expect

(2).should_not.be.equal(3)
(2).shouldnt.be.equal(3)
(2).doesnt.equals(3)
(2).does_not.equals(3)
(2).doesnot.equals(3)
(2).dont.equal(3)
(2).do_not.equal(3)

expect(3).to.not_be.equal(1)
```

## Chain-up synonyms

Any of those synonyms work as an alias to the assertion builder:

* `be`
* `being`
* `to`
* `when`
* `have`
* `with_value`

```python
from sure import expect

{"foo": 1}.must.with_value.being.equal({"foo": 1})
{"foo": 1}.does.have.key("foo").being.with_value.equal(1)
```

## Equality synonyms

```python

(2).should.equal(2)
(2).should.equals(2)
(2).should.eql(2)
```

## Positive boolean synonyms

```python

(not None).should.be.ok
(not None).should.be.truthy
(not None).should.be.true
```

## Negative boolean synonyms

```python
False.should.be.falsy
False.should.be.false
False.should_not.be.true
False.should_not.be.ok
None.should_not.be.true
None.should_not.be.ok
```


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

The assertion library is 100% inspired be the awesomeness of
[should.js](https://github.com/visionmedia/should.js) which is simple,
declarative and fluent.

Sure strives to provide everything a python developer needs in an assertion:

* Assertion messages are easy to understand

* When comparing iterables the comparation is recursive and shows
  exactly where is the error

* Fluency: the builtin types are changed in order to provide awesome
  simple assertions
