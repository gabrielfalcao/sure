.. _sure:

Sure
====
.. index:: sure

.. _Introduction:

Introduction
------------

Sure is a both a library and a test-runner for for the Python Programming Languages, featuring a DSL for writing
assertions. Sure's original author is `Gabriel Falcão <https://github.com/gabrielfalcao>`_.

Sure provides a :ref:`Special Syntax` for writing tests in a
human-friendly, fluent and easy-to-use manner, In the context of the
Python Programming language, Sure is a pioneer at extending every
object with test-specific methods at test-runtime. This feature is
disabled by default starting on version 3.0.0 and MAY be optionally
enabled programmatically or via command-line. Read the section
:ref:`Special Syntax` for more information.

Whether the :ref:`Special Syntax` is enabled or not, :ref:`sure`
generally aims at enabling software developers to writing tests in a
human-friendly, fluent and hopefully fun way.


Quick Examples
--------------

:ref:`Standard Behavior` Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   from sure import expect

   def printing_money_indiscriminately(amount):
       raise ValueError(f"Inflation! Printing {amount} amounts of money is likely increase inflation!")

   expect(printing_money_indiscriminately.when.called_with(88888888).should.throw(
       ValueError,
       "Inflation! Printing 88888888 amounts of money is likely increase inflation!"
   )


:ref:`Special Syntax` Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

   import sure
   sure.enable_special_syntax()

   def superpowers(mode):
       if mode in ("ignorance", "selfishness"):
           raise SyntaxError(
               f"superpowers cannot, must not and shall not be used in the name of {mode}!"
           )
        raise NotImplementedError(
            f"{mode} entirely not allowed"
        )

   superpowers.when.called_with("ignorance").should.have.raised(
       SyntaxError,
       "superpowers cannot, must not and shall not be used in the name of ignorance!"
   )

   superpowers.when.called_with("selfishness").should.have.raised(
       SyntaxError,
       "superpowers cannot, must not and shall not be used in the name of selfishness!"
   )

   superpowers.when.called_with("out thinking").should.have.raised(
       NotImplementedError,
       "out thinking entirely not allowed"
   )
