sure ``1.2.24``
===============

A testing library for python with powerful and flexible assertions. Sure
is heavily inspired by
`should.js <https://github.com/visionmedia/should.js/>`__

|Build Status|

Installing
==========

::

    user@machine:~$ [sudo] pip install sure

Documentation
=============

Available in the `website <http://falcao.it/sure>`__ or under the
``spec`` directory.

You can also build the documentation locally using markment:

.. code:: bash

    pip install markment
    markment --server --theme=rtd ./spec/

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
