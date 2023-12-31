.. _Assertion Builder Reference:

Assertion Builder Reference
===========================

Numerical Equality
------------------

``(2 + 2).should.equal(4)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python


   (4).should.be.equal(2 + 2)
   (7.5).should.eql(3.5 + 4)
   (2).should.equal(8 / 4)

   (3).shouldnt.be.equal(5)


``.equal(float, epsilon)``
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python


   (4.242423).should.be.equal(4.242420, epsilon=0.000005)
   (4.01).should.be.eql(4.00, epsilon=0.01)
   (6.3699999).should.equal(6.37, epsilon=0.001)

   (4.242423).shouldnt.be.equal(4.249000, epsilon=0.000005)


String Equality
---------------

``.should_not.be.different_of(string)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python


   XML1 = '''<root>
     <a-tag with-attribute="one">AND A VALUE</a-tag>
   </root>'''


   XML1.should_not.be.different_of(XML1)

   XML2 = '''<root>
     <a-tag with-attribute="two">AND A VALUE</a-tag>
   </root>'''

   XML2.should.be.different_of(XML1)

The code above should present an output containing a diff like below:

.. code:: bash

   Difference:

   <root>
   -   <a-tag with-attribute="one">AND A VALUE</a-tag>
   ?                           --
   +   <a-tag with-attribute="two">AND A VALUE</a-tag>
   ?                          ++
   </root>

``.should.equal("a string")``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   "Awesome ASSERTIONS".lower().split().should.equal(['awesome', 'assertions'])


String Similarity
-----------------

``.look_like()``
~~~~~~~~~~~~~~~~

.. code:: python


   """
   THIS IS MY loose string
   """.should.look_like('this is my loose string')

   """this one is different""".should_not.look_like('this is my loose string')


Regular-Expressions
-------------------

:ref:`Sure` supports testing strings against regular expressions via :mod:`re`

``should.match()``
~~~~~~~~~~~~~~~~~~

You can also use the modifiers:

-  `re.DEBUG <https://docs.python.org/2/library/re.html#re.DEBUG>`__
-  `re.I and re.IGNORECASE <https://docs.python.org/2/library/re.html#re.IGNORECASE>`_
-  `re.M and re.MULTILINE <https://docs.python.org/2/library/re.html#re.MULTILINE>`_
-  `re.S re.DOTALL <https://docs.python.org/2/library/re.html#re.DOTALL>`_
-  `re.U and re.UNICODE <https://docs.python.org/2/library/re.html#re.UNICODE>`_
-  `re.X and re.VERBOSE <https://docs.python.org/2/library/re.html#re.VERBOSE>`_

.. code:: python

   import re

   "SOME STRING".should.match(r'some \w+', re.I)
   "FOO BAR CHUCK NORRIS".should_not.match(r'some \w+', re.M)

.. _Collections or Iterables:

Collections or Iterables
------------------------

The following set of assertion methods work with the following kinds
of data-structures or iterable objects:

- Array-like structures: :class:`list`, :class:`tuple`, :class:`set`, :class:`frozenset` etc
- Key-Value structures: :class:`dict`, :class:`collections.OrderedDict` etc
- Any valid implementation of :ref:`python:iterator`


``.equal({'a': 'collection'})``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Performs :ref:`deep comparison <Deep Comparison>` of :ref:`collections or iterables <Collections or Iterables>`

.. code:: python

    {'foo': 'bar'}.should.equal({'foo': 'bar'})
    {'foo': 'bar'}.should.eql({'foo': 'bar'})
    {'foo': 'bar'}.must.be.equal({'foo': 'bar'})


``.contain()``
~~~~~~~~~~~~~~

``expect(collection).to.contain(item)`` is a shorthand to
``expect(item).to.be.within(collection)``

.. code:: python

    ['1.2.5', '1.2.4'].should.contain('1.2.5')
    '1.2.4'].should.be.within(['1.2.5', '1.2.4'])

    # also works with strings
    "My bucket of text".should.contain('bucket')
    "life".should_not.contain('anger')
    '1.2.3'.should.contain('2')


``.should.be.empty``
~~~~~~~~~~~~~~~~~~~~

.. code:: python


    [].should.be.empty
    {}.should.be.empty
    set().should.be.empty
    "".should.be.empty
    ().should.be.empty
    range(0).should.be.empty

    ## negate with:

    [1, 2, 3].shouldnt.be.empty
    "Dummy String".shouldnt.be.empty
    "Dummy String".should_not.be.empty


.. should_be_within:

``{number}.should.be.within(0, 10)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

asserts inclusive numeric range

.. code:: python

    (1).should.be.within(0, 2)
    (5).should.be.within(0, 10)

    ## negate with:

    (1).shouldnt.be.within(5, 6)


``.be.within({iterable})``
~~~~~~~~~~~~~~~~~~~~~~~~~~

asserts that a member is part of the iterable

.. code:: python

    "G".should.be.within("gabriel".capitalize())
    "g".should.be.within("gabriel")
    'name'.should.be.within({'name': 'Gabriel'})
    'peace'.should.be.within(['world', 'peace'])

    ## negate with:

    'war'.should_not.be.within(['cosmos', 'universe', 'world'])
    'Bug'.shouldnt.be.within(['Sure 1.0'])
    'Bug'.should_not.be.within(['Sure 1.0'])


``.be.none``
~~~~~~~~~~~~

Assert whether an object is or not ``None``

.. code:: python


    value = None
    value.should.be.none
    None.should.be.none

    "".should_not.be.none
    (not None).should_not.be.none

``.be.ok``
~~~~~~~~~~

Assert truthfulness:

.. code:: python

    from sure import this

    True.should.be.ok
    'truthy string'.should.be.ok
    {'truthy': 'dictionary'}.should.be.ok

And negate truthfulness:

.. code:: python


    from sure import this

    False.shouldnt.be.ok
    ''.should_not.be.ok
    {}.shouldnot.be.ok


``.have.property()``
~~~~~~~~~~~~~~~~~~~~

.. code:: python


    class Basket(object):
        fruits = ["apple", "banana"]


    basket1 = Basket()

    basket1.should.have.property("fruits")


``.have.property().being.*``
............................

If the programmer calls ``have.property()`` it returns an assertion
builder of the property if it exists, so that you can chain up
assertions for the property value itself.

.. code:: python

    class Basket(object):
        fruits = ["apple", "banana"]

    basket2 = Basket()
    basket2.should.have.property("fruits").which.should.be.equal(["apple", "banana"])
    basket2.should.have.property("fruits").being.equal(["apple", "banana"])
    basket2.should.have.property("fruits").with_value.equal(["apple", "banana"])
    basket2.should.have.property("fruits").with_value.being.equal(["apple", "banana"])

``.have.key()``
~~~~~~~~~~~~~~~

.. code:: python

    basket3 = dict(fruits=["apple", "banana"])
    basket3.should.have.key("fruits")

``.have.key().being.*``
.......................

If the programmer calls ``have.key()`` it returns an assertion builder
of the key if it exists, so that you can chain up assertions for the
dictionary key value itself.

.. code:: python

    person = dict(name=None)
    person.should.have.key("name").being.none
    person.should.have.key("name").being.equal(None)


``.have.length_of(2)``
~~~~~~~~~~~~~~~~~~~~~~

Assert the length of objects

.. code:: python


    [3, 4].should.have.length_of(2)

    "Python".should.have.length_of(6)

    {'john': 'person'}.should_not.have.length_of(2)


``{X}.should.be.greater_than(Y) and {Y}.should.be.lower_than(X)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assert the magnitude of objects with ``{X}.should.be.greater_than(Y)`` and ``{Y}.should.be.lower_than(X)`` as well as ``{X}.should.be.greater_than_or_equal_to(Y)`` and ``{Y}.should.be.lower_than_or_equal_to(X)``.


.. code:: python

    (5).should.be.greater_than(4)
    (5).should_not.be.greater_than(10)
    (1).should.be.lower_than(2)
    (1).should_not.be.lower_than(0)

    (5).should.be.greater_than_or_equal_to(4)
    (5).should_not.be.greater_than_or_equal_to(10)
    (1).should.be.lower_than_or_equal_to(2)
    (1).should_not.be.lower_than_or_equal_to(0)


Testing Callables
-----------------


``callable.when.called_with(arg1, kwarg1=2).should.have.raised(Exception)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use this feature to assert that a callable raises an exception:

.. code:: python

    range.when.called_with("chuck norris").should.have.raised(TypeError)
    range.when.called_with(10).should_not.throw(TypeError)

Regular Expression matching on the exception message
....................................................

You can also match regular expressions with to the expected exception
messages:

.. code:: python

    import re
    range.when.called_with(10, step=20).should.have.raised(TypeError, re.compile(r'(does not take|takes no) keyword arguments'))
    range.when.called_with("chuck norris").should.have.raised(TypeError, re.compile(r'(cannot be interpreted as an integer|integer end argument expected)'))


``.should.throw(Exception)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An idiomatic alias to ``.should.have.raised``.

.. code:: python

    range.when.called_with(10, step="20").should.throw(TypeError, "range() takes no keyword arguments")
    range.when.called_with(b"chuck norris").should.throw("range() integer end argument expected, got str.")


``function.when.called_with(arg1, kwarg1=2).should.return_value(value)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a shorthand for testing that a callable returns the expected
result

.. code:: python

    list.when.called_with([0, 1]).should.have.returned_the_value([0, 1])

which equates to:

::

    value = range(2)
    value.should.equal([0, 1])

there are no differences between those 2 possibilities, use at will

``.be.a('typename')``
~~~~~~~~~~~~~~~~~~~~~

this takes a type name and checks if the class matches that name

.. code:: python


    {}.should.be.a('dict')
    (5).should.be.an('int')

    ## also works with paths to modules

    range(10).should.be.a('collections.Iterable')

``.be.a(type)``
~~~~~~~~~~~~~~~

this takes the class (type) itself and checks if the object is an
instance of it

.. code:: python

    from six import PY3

    if PY3:
        u"".should.be.an(str)
    else:
        u"".should.be.an(unicode)
    [].should.be.a(list)

``.be.above(num) and .be.below(num)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

assert the instance value above and below ``num``

.. code:: python


    (10).should.be.below(11)
    (10).should.be.above(9)
    (10).should_not.be.above(11)
    (10).should_not.be.below(9)


Too long, didn't read
~~~~~~~~~~~~~~~~~~~~~


All those possibilities below work just as the same
...................................................

.. code:: python

    from sure import it, this, those, these

    (10).should.be.equal(5 + 5)

    this(10).should.be.equal(5 + 5)
    it(10).should.be.equal(5 + 5)
    these(10).should.be.equal(5 + 5)
    those(10).should.be.equal(5 + 5)


Also if you prefer using the assert keyword in your tests just go ahead an do it!
.................................................................................

Every assertion returns ``True`` when succeeded, and if failed the
AssertionError is already raised internally by sure, with a nice
description of what failed to match, too.

.. code:: python

    from sure import it, this, those, these, expect

    assert (10).should.be.equal(5 + 5)
    assert this(10).should.be.equal(5 + 5)
    assert it(10).should.be.equal(5 + 5)
    assert these(10).should.be.equal(5 + 5)
    assert those(10).should.be.equal(5 + 5)

    expect(10).to.be.equal(5 + 5)
    expect(10).to.not_be.equal(8)

``(lambda: None).should.be.callable``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test if something is or not callable

.. code:: python


    range.should.be.callable
    (lambda: None).should.be.callable
    (123).should_not.be.callable


A note about the ``assert`` keyword
...................................

.. note:: *you can use or not the* ``assert`` *keyword, sure
          internally already raises an appropriate* ``AssertionError`` *with an
          assertion message so that you don't have to specify your own, but you
          can still use* ``assert`` *if you find it more semantic*

Examples:

.. code:: python


    "Name".lower().should.equal('name')

    # or

    assert "Name".lower().should.equal('name')

    # or

    from sure import this

    assert this("Name".lower()).should.equal('name')

    ## also without the assert

    this("Name".lower()).should.equal('name')

Any of the examples above will raise their own ``AssertionError`` with a
meaningful error message.

Synonyms
--------

Sure provides you with a lot of synonyms so that you can pick the ones
that makes more sense for your tests.

Note that the examples below are merely illustrative, they work not only
with numbers but with any of the assertions you read early in this
documentation.

Positive synonyms
~~~~~~~~~~~~~~~~~

.. code:: python


    (2 + 2).should.be.equal(4)
    (2 + 2).must.be.equal(4)
    (2 + 2).does.equals(4)
    (2 + 2).do.equals(4)

Negative synonyms
~~~~~~~~~~~~~~~~~

.. code:: python

    from sure import expect

    (2).should_not.be.equal(3)
    (2).shouldnt.be.equal(3)
    (2).doesnt.equals(3)
    (2).does_not.equals(3)
    (2).doesnot.equals(3)
    (2).dont.equal(3)
    (2).do_not.equal(3)

    expect(3).to.not_be.equal(1)

Chain-up synonyms
~~~~~~~~~~~~~~~~~

Any of those synonyms work as an alias to the assertion builder:

-  ``be``
-  ``being``
-  ``to``
-  ``when``
-  ``have``
-  ``with_value``

.. code:: python

    from sure import expect

    {"foo": 1}.must.with_value.being.equal({"foo": 1})
    {"foo": 1}.does.have.key("foo").being.with_value.equal(1)

Equality synonyms
~~~~~~~~~~~~~~~~~

.. code:: python


    (2).should.equal(2)
    (2).should.equals(2)
    (2).should.eql(2)


Positive boolean synonyms
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    (not False).should.be.ok
    (not None).should.be.truthy
    True.should.be.true
    (7 * 8 == 72).should.be.true

Negative boolean synonyms
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    False.should.be.falsy
    False.should.be.false
    False.should_not.be.true
    False.should_not.be.ok
    None.should_not.be.true
    None.should_not.be.ok

Add custom assertions, chains and chain properties
--------------------------------------------------

``sure`` allows to add custom assertion methods, chain methods and chain properties.

Custom assertion methods
~~~~~~~~~~~~~~~~~~~~~~~~

By default :ref:`sure` comes with a good amount of *assertion methods*. For example:

- ``equals()``
- ``within()``
- ``contains()``

And plenty more.

However, in some cases it makes sense to add custom *assertion methods* to improve the test experience.

Let's assume you want to test your web application. Somewhere there is a ``Response`` class with a ``return_code`` property. We could do the following:

.. code:: python

   response = Response(...)
   response.return_code.should.be.equal(200)

This is already quiet readable, but wouldn't it be awesome do to something like this:

.. code:: python

   response = Response(...)
   response.should.have.return_code(200)

To achieve this the custom assertion methods come into play:

.. code:: python

   from sure import assertion

   @assertion
   def return_code(self, expected_return_code):
       if self.negative:
           assert expected_return_code != self.obj.return_code, \
               'Expected return code matches'
       else:
           assert expected_return_code == self.obj.return_code, \
               'Expected return code does not match'


   response = Response(...)
   response.should.have.return_code(200)


I'll admit you have to write the assertion method yourself, but the result is a great experience you don't want to miss.


Chain methods
~~~~~~~~~~~~~

*chain methods* are similar to *assertion methods*. The only difference is that the *chain methods*, as the name implies, can be chained with further chains or assertions:

.. code:: python

   from sure import chain

   @chain
   def header(self, header_name):
       # check if header name actually exists
       self.obj.headers.should.have.key(header_name)
       # return header value
       return self.obj.headers[header_name]


   response = Response(200, headers={'Content-Type': 'text/python'})
   response.should.have.header('Content-Type').equals('text/python')


Chain properties
~~~~~~~~~~~~~~~~

*chain properties* are simple properties which are available to build an assertion.
Some of the default chain properties are:

- ``be``
- ``to``
- ``when``
- ``have``
- ...

Use the ``chainproperty`` decorator like the following to build your own *chain*:

.. code:: python

   from sure import chainproperty, assertion


   class Foo:
       special = 42


   @chainproperty
   def having(self):
       return self


   @chainproperty
   def implement(self):
       return self


   @assertion
   def attribute(self, name):
       has_it = hasattr(self.obj, name)
       if self.negative:
           assert not has_it, 'Expected was that object {0} does not have attr {1}'.format(
               self.obj, name)
       else:
           assert has_it, 'Expected was that object {0} has attr {1}'.format(
               self.obj, name)

   # Build awesome assertion chains
   expect(Foo).having.attribute('special')
   Foo.doesnt.implement.attribute('nospecial')

Use custom assertion messages with ``ensure``
---------------------------------------------

With the ``ensure`` context manager *sure* provides an easy to use way to override the ``AssertionError`` message raised by ``sure``'s assertion methods. See the following example:

.. code:: python


    name = myapi.do_something_that_returns_string()

    with sure.ensure('the return value actually looks like: {0}', name):
        name.should.contain('whatever')


In case ``name`` does not contain the string ``whatever`` it will raise an ``AssertionError`` exception
with the message *the return value actually looks like: <NAME>* (where *<NAME>* would be the actual value of the variable ``name``) instead of *sure*'s default error message in that particular case.

Only ``AssertionError`` exceptions are re-raised by ``sure.ensure()`` with the custom provided message. Every other exception will be ignored and handled as expected.
