.. _Getting Started:

Getting Started
===============

Installing
----------

It is available in PyPi, so you can install through pip:

.. code:: bash

   pip install sure


Python version compatibility
----------------------------

:ref:`sure` is `continuously tested against
<https://github.com/gabrielfalcao/sure/actions?query=workflow%3A%22Sure+Tests%22>`__
python versions 3.6, 3.7, 3.9, 3.10 and 3.11 of the `cpython
<https://github.com/python/cpython/>`_ implementation. It is not
unlikely to work with other Python implementations such as `PyPy
<https://pypy.org/>`_ or `Jython <https://www.jython.org/>`_ with the
added caveat that its :ref:`Special Syntax` is most likely to **not
work** in any implementations other than `cpython
<https://github.com/python/cpython/>`_ while the :ref:`Standard
Behavior` is likely to work well.


:ref:`Standard Behavior` Example
--------------------------------

.. code:: python

   from sure import expect

   expect("this".replace("is", "at")).to.equal("that")


:ref:`Special Syntax` Example (cpython-only)
--------------------------------------------

.. code:: python

   "this".replace("is", "at").should.equal("that")


.. note::
   The :ref:`Special Syntax` can be enabled via command-line with the
   ``--special-syntax`` flag or programmatically with the statement
   ``sure.enable_special_syntax()``
