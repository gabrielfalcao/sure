.. _How Sure Works:

How it :ref:`Sure` works
========================

As an automated testing library
-------------------------------

.. _Standard Behavior:

Standard Behavior
~~~~~~~~~~~~~~~~~

.. seealso:: The section :ref:`Assertion Builder Reference` presents a vast set of practical examples

At the most basic level, :ref:`sure` provides "assertion builder"
which take a "source" object and contain methods to articulate
different forms of comparison against a "destination" object.

The value of each type of comparison depends upon the value types of
entire objects themselves or a portion of them, each case depends both
on the value type and the chosen method of comparison. More on that
soon.

Before explaining the behavior and mechanics of assertion builders at
length it might be valuable to acquaint oneself with the list of all
of Sure's builtin assertion builders exemplified in Python import
statements below:

.. code:: python

   from sure import assert_that
   from sure import it
   from sure import expect
   from sure import expects
   from sure import that
   from sure import the
   from sure import these
   from sure import this
   from sure import those


Each of the imports above are, in fact, instances of the class
:class:`~sure.AssertionBuilder`.

Instances of :class:`~sure.AssertionBuilder` provide a vast set of
assertion methods that, as mentioned previously, are composed by two
objects to be compared, referred to as either "source" and
"destination" objects in this documentation or ``X`` and ``Y``
identifiers at the error message introductions of failed assertions
and should be literally understood in terms of logical variables -
placeholders for values which are not yet known or clear at the moment
of test verification - that intend to render intelligible and indicate
clearly the the differences between values by themselves or within
data-structures such as :ref:`sequences <python:sequence>`,
:ref:`mappings <python:mapping>` or :ref:`iterable objects
<python:iterator>`.

In this latter case, the logical variables ``X`` and ``Y`` MAY be
accompanied by what resembles Python's slicing notation, indicating
the location of different values within their corresponding
data-structures.


A Detailed Example of Assertion Builders
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code-block:: python
   :emphasize-lines: 8,10,12

   import unittest
   from sure import assert_that, that

   class AssertionBuilderExample(unittest.TestCase):
       def test_numerical_value_comparison(self):
           """the statements below should be reasonably equivalent in some aspects"""

           assert_that(2).should.be.lower_than(3)

           assert_that(2 < 3).should.equal(True)

           assert_that(2 < 3).should.be.true

    if __name__ == "__main__":
        unittest.run()

Notice that every assertion in the example above is performing the same logical comparison: that the numerical value ``2`` is arithmetically lower than ``3``.

The first assertion performed with :attr:`~sure.assert_that` take the
value ``2`` (a :class:`int` object) as the "source" object:
``assert_that(2)`` at which point that particular instance of
:class:`AssertionBuilder` requires an assertion to be built upon
itself, accomplished in the rest of that statement -
``.should.be.lower_than(3)`` - where the value ``3`` is the
"destination" object.

The two remaining examples in this particular example take boolean
values (:class:`bool` objects) as "source" and "destination" objects.

The statement ``assert_that(2 < 3).should.equal(True)``
the assertion builder takes the expression ``2 < 3`` as the "source"
object and the literal value ``True`` as the destination object.

Because the expected value is clearly provided in both of the cases
above, it is correct to think of destination objects as "explicit".

The third and last statement, in contrast to the first two just
explained, relies on the internal mechanics of the ``.should.be.true``
statement, which ends with a call to the
:attr:`~sure.AssertionBuilder.true` which is a
:func:`python:property`-decorated function that checks for logical
proof that the "source" object exactly equivalent to the
:py:class:`bool` ``True``.


.. _Special Syntax:

Special Syntax
~~~~~~~~~~~~~~

The :ref:`sure` module presents the concept of "special syntax"
defined as the optional feature of, during runtime, extending every
:class:`object` with assertion methods with the purpose of enabling
a kind of fluent writing of automated tests.


First, a bit of history
.......................

From Sure's absolute ideation, its original author - Gabriel Falcão -
had envisioned to somehow expand Python's :class:`object` with
assertion methods during test runtime so that software engineers,
coders or developers in general could benefit from somewhat more
human-friendly and fluent assertions in the sense of literal writing
fluency. At any rate, after much brainstorming, the best solution
Gabriel could come up with was to provide a Python class -
:class:`sure.AssertionBuilder` - where and whence friendly
assertions could be built upon.

Gabriel crafted the :class:`sure.AssertionBuilder` in such way that
its usage could seem like verbs or adverbs so as to work with or
without Python's ``assert`` statement. But even more so than that, the
during the crafting of the :class:`sure.AssertionBuilder` it was
kept in mind that if it were possible to "hack" Python's syntax to
inject methods such as ``.should``, ``.should_not``, ``.must``,
``.must_not``, ``.shouldnt`` and ``.mustnt`` into :class:`object`
during **test runtime only**, then :class:`sure.AssertionBuilder`
could be almost effortlessly leveraged within those method's
implementations.

To be sure - pun intended - Gabriel crafted the
:class:`sure.AssertionBuilder` such that its assertion methods
always returned ``True`` so that ``assert`` statements such as
``assert that(X).is_not(Y)`` where ``X = False`` and ``Y = True``,
would return ``True`` even in an occasion when, in this case, both
``X`` and ``Y`` were either ``True`` or ``False``.

Gabriel's purpose was not to allow or enable abuse of assertions but
to prevent Python from raising a :exc:`AssertionError` with no
details and instead bring as much detail as possible in the occasion
of such exception, to the point of doing its best to show at what key
or what index there is a difference in the case of testing equality
between the datastructures :class:`dict` or :class:`list`,
respectivelly in this case. (See :class:`sure.Explanation` for more)

Gabriel's initial idea came from believing that other programming
languages suchs as Ruby or Javascript had tools or libraries such as
`RSpec <https://rspec.info/>`_ or `Should.js
<https://shouldjs.github.io/>`_ which provided a kind of syntax-sugar
that seemed much more appealing or inviting for developers, making the
process of writing tests more pleasant, rewarding or fun in sort of way.

At the time of Sure's inception, so to speak, which was around
the middle of the year of 2010, the testing tools for the Ruby programming language seemed
much more mature and the market seemed to be booming with innovative, stable and resilient products `crafted <https://en.wikipedia.org/wiki/Software_craftsmanship>`_ by `practicioners of Agile Methodologies <https://en.wikipedia.org/wiki/Agile_software_development>`_

Around the year of 2012 Gabriel Falcão was working at a startup in NYC
and recruited two colleagues, one of whom was Lincoln Clarete which
had been known to Gabriel to know quite a bit about the internals of
the Python language. Then Gabriel not so much as asked whether it was
possible to inject methods into :class:`object` during runtime but
actually challenged Lincoln to do try and do so.

As Gabriel imagined, it wouldn't take long for Lincoln Clarete to
achieve that goal, he then presently wrote most if not all the code
currently present inside :mod:`sure.special` and also took the idea
forward and evolvend it, ultimately resulting in the publishing of the
Python Package `forbidden fruit
<https://clarete.github.io/forbiddenfruit/>`_.

Nevertheless, there is a caveat regarding the functionallity provided
by such :ref:`Special Syntax`: it is primarily supposed to work only
with `cpython <https://github.com/python/cpython/>`_, the standard
implementation of the Python programming language in the C programming
language. This is because :ref:`sure` depends on the `ctypes
<https://docs.python.org/library/ctypes>`_ module to gain write-access
to the ``__dict__`` member of :class:`object` during (test) runtime.

More precisely, it is worth noting that whether the `ctypes
<https://docs.python.org/library/ctypes>`_ library or an equivalent is
available to other implementations of Python such as `Jython
<https://www.jython.org/>`__, only the CPython provide
```ctypes.pythonapi``
<https://docs.python.org/library/ctypes#loading-shared-libraries>`__
the features required by Sure.


Chainability
............

Some specific assertion methods are chainable, it can be useful for
short assertions like:

.. code:: python

   PERSON = {
     "name": "John",
     "facebook_info": {
       "token": "abcd"
     }
   }

   PERSON.should.have.key("facebook_info").being.a(dict)
