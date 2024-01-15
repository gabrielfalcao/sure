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

The sophisticated automated test tool for Python, featuring a test
runner and a library with powerful and flexible assertions.

Originally authored by `Gabriel Falcão <https://github.com/gabrielfalcao>`_.


Installing
----------

.. code:: bash

   pip install sure


Running tests
-------------

.. code:: bash

   sure tests


For More Information:

.. code:: bash

   sure --help


Documentation
-------------

Available on the `website <https://sure.readthedocs.io/en/latest/>`_.

To build locally run:

.. code:: bash

    make docs


Quick Library Showcase
----------------------

.. code:: python

   from sure import expects

   expects(4).to.be.equal(2 + 2)
   expects(7.5).to.be.eql(3.5 + 4)

   expects(3).to.not_be.equal(5)
   expects(9).to_not.be.equal(11)

.. code:: python

   from sure import expects

   expects({'foo': 'bar'}).to.equal({'foo': 'bar'})
   expects({'foo': 'bar'}).to.have.key('foo').being.equal('bar')

.. code:: python

   "Awesome ASSERTIONS".lower().split().should.equal(['awesome', 'assertions'])
