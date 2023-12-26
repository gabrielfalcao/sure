How sure works
==============

The class ``sure.AssertionBuilder`` creates objects capable of doing
assertions. The AssertionBuilder simply arranges a vast set of possible
assertions that are composed by a ``source`` object and a
``destination`` object.

Every assertion, even implicitly if implicitly like in
``(2 < 3).should.be.true``, is doing a source/destination matching.

Chainability
------------

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

A bit of history
================

From Sure's absolute ideation, its original author - Gabriel Falcão -
had envisioned to somehow expand Python's :py:class:`object` with
assertion methods during test runtime so that software engineers,
coders or developers in general could benefit from somewhat more
human-friendly and fluent assertions in the sense of literal writing
fluency. At any rate, after much brainstorming, the best solution
Gabriel could come up with was to provide a Python class -
:py:class:`sure.AssertionBuilder` - where and whence friendly
assertions could be built upon.

Gabriel crafted the :py:class:`sure.AssertionBuilder` in such way that
its usage could seem like verbs or adverbs so as to work with or
without Python's ``assert`` statement. But even more so than that, the
during the crafting of the :py:class:`sure.AssertionBuilder` it was
kept in mind that if it were possible to "hack" Python's syntax to
inject methods such as ``.should``, ``.should_not``, ``.must``,
``.must_not``, ``.shouldnt`` and ``.mustnt`` into :py:class:`object`
during **test runtime only**, then :py:class:`sure.AssertionBuilder`
could be almost effortlessly leveraged within those method's
implementations.

To be sure - pun intended - Gabriel crafted the
:py:class:`sure.AssertionBuilder` such that its assertion methods
always returned ``True`` so that ``assert`` statements such as
``assert that(X).is_not(Y)`` where ``X = False`` and ``Y = True``,
would return ``True`` even in an occasion when, in this case, both
``X`` and ``Y`` were either ``True`` or ``False``.

Gabriel's purpose was not to allow or enable abuse of assertions but
to prevent Python from raising a :py:class:`AssertionError` with no
details and instead bring as much detail as possible in the occasion
of such exception, to the point of doing its best to show at what key
or what index there is a difference in the case of testing equality
between the datastructures :py:class:`dict` or :py:class:`list`,
respectivelly in this case. (See :py:class:`sure.DeepExplanation` for more)

Gabriel's initial idea came from believing that other programming
languages suchs as Ruby or Javascript had tools or libraries such as
RSpec or Should.js which provided a kind of syntax-sugar that seemed
much more appealing or inviting for developers, making the process of
writing tests more pleasant or rewarding.

At the time of Sure's inception, so to speak, which was around
the middle of the year of 2010, the testing tools for the Ruby programming language seemed
much more mature and the market seemed to be booming with innovative, stable and resilient products `crafted <https://en.wikipedia.org/wiki/Software_craftsmanship>`_ by `practicioners of Agile Methodologies <https://en.wikipedia.org/wiki/Agile_software_development>`_

Around the year of 2012 Gabriel Falcão was working at a startup in NYC
and recruited two colleagues, one of whom was Lincoln Clarete which
had been known to Gabriel to know quite a bit about the internals of
the Python language. Then Gabriel not so much as asked whether it was
possible to inject methods into :py:class:`object` during runtime but
actually challenged Lincoln to do try and do so.

As Gabriel imagined, it wouldn't take long for Lincoln Clarete to
achieve that goal, he then presently wrote most if not all the code
currently present inside :py:mod:`sure.magic` and also took the idea
forward and evolvend it, ultimately resulting in the publishing of the
Python Package `forbidden fruit
<http://clarete.github.io/forbiddenfruit/>`_.

The only catch is that the functionallity inside :py:mod:`sure.magic`
is primarily guaranteed to work only with CPython, the original
implementation of Python in the C programming language.

Why CPython-only ?
------------------

Sure uses the `ctypes <http://docs.python.org/library/ctypes>`_ module
to gain write-access to the ``__dict__`` of :py:class:`object` at runtime.

Although `ctypes <http://docs.python.org/library/ctypes>`_ might also be available in other implementations such as
`Jython <http://www.jython.org/>`__, only the CPython  provide
```ctypes.pythonapi`` <http://docs.python.org/library/ctypes#loading-shared-libraries>`__
the features required by Sure.
