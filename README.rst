sure
====

.. image:: https://img.shields.io/pypi/dm/sure
   :target: https://pypi.org/project/sure

.. image:: https://github.com/gabrielfalcao/sure/workflows/Sure%20Tests/badge.svg
   :target: https://github.com/gabrielfalcao/sure/actions?query=workflow%3A%22Sure+Tests%22

.. image:: https://img.shields.io/readthedocs/sure
   :target: https://sure.readthedocs.io/

.. image:: https://img.shields.io/github/license/gabrielfalcao/sure?label=Github%20License
   :target: https://github.com/gabrielfalcao/sure/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/v/sure
   :target: https://pypi.org/project/sure

.. image:: https://img.shields.io/pypi/l/sure?label=PyPi%20License
   :target: https://pypi.org/project/sure

.. image:: https://img.shields.io/pypi/format/sure
   :target: https://pypi.org/project/sure

.. image:: https://img.shields.io/pypi/status/sure
   :target: https://pypi.org/project/sure

.. image:: https://img.shields.io/pypi/pyversions/sure
   :target: https://pypi.org/project/sure

.. image:: https://img.shields.io/pypi/implementation/sure
   :target: https://pypi.org/project/sure

.. image:: https://img.shields.io/github/v/tag/gabrielfalcao/sure
   :target: https://github.com/gabrielfalcao/sure/releases

.. image:: https://img.shields.io/badge/pydoc-web-ff69b4.svg
   :target: http://pydoc.net/sure

An idiomatic testing library for python with powerful and flexible assertions, created by `Gabriel Falcão <https://github.com/gabrielfalcao>`_.
Sure's developer experience is inspired and modeled after `RSpec Expectations
<http://rspec.info/documentation/3.5/rspec-expectations/>`_ and
`should.js <https://github.com/shouldjs/should.js>`_.

Installing
----------

.. code:: bash

    $ pip install sure

Documentation
-------------

Available in the `website <https://sure.readthedocs.io/en/latest/>`__ or under the
``docs`` directory.

You can also build the documentation locally using sphinx:

.. code:: bash

    make docs

Here is a tease
---------------

Equality
~~~~~~~~

(number).should.equal(number)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    import sure

    (4).should.be.equal(2 + 2)
    (7.5).should.eql(3.5 + 4)

    (3).shouldnt.be.equal(5)

Assert dictionary and its contents
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    {'foo': 'bar'}.should.equal({'foo': 'bar'})
    {'foo': 'bar'}.should.have.key('foo').which.should.equal('bar')

"A string".lower().should.equal("a string") also works
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    "Awesome ASSERTIONS".lower().split().should.equal(['awesome', 'assertions'])
