sure
====

An idiomatic testing library for python with powerful and flexible assertions. Sure
is heavily inspired in `RSpec Expectations <http://rspec.info/documentation/3.5/rspec-expectations/>`_ and `should.js <https://github.com/shouldjs/should.js>`_

|Build Status| |PyPI package version| |PyPI python versions| |Join the chat at https://gitter.im/gabrielfalcao/sure|


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

.. |Build Status| image:: https://travis-ci.org/gabrielfalcao/sure.png?branch=master
   :target: https://travis-ci.org/gabrielfalcao/sure
.. |PyPI package version| image:: https://badge.fury.io/py/sure.svg
   :target: https://badge.fury.io/py/sure
.. |PyPI python versions| image:: https://img.shields.io/pypi/pyversions/sure.svg
   :target: https://pypi.python.org/pypi/sure
.. |Join the chat at https://gitter.im/gabrielfalcao/sure| image:: https://badges.gitter.im/gabrielfalcao/sure.svg
   :target: https://gitter.im/gabrielfalcao/sure?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
