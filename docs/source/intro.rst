Introduction
============

Sure is a python library for python that leverages a DSL for writing
assertions created by `Gabriel Falcão <https://github.com/gabrielfalcao>`_.

In CPython it monkey-patches the ``object`` type, adding some methods
and properties purely for test purposes.

Any python code writen after ``import sure`` gains testing superpowers,
so you can write assertions like this:

.. code:: python

    import sure


    def some_bratty_function(parameter):
        raise ValueError("Me no likey {0}".format(parameter))


    some_bratty_function.when.called_with("Scooby").should.throw(ValueError, "Me no likey Scooby")

Let's `get it started <getting-started.html>`__
