Change Log
==========

All notable changes to this project will be documented in this file.
This project adheres to `Semantic Versioning <http://semver.org/>`__.

[v3.0.0]
--------

-  Presents better documentation
-  Drops support to Python 2 obliterates the ``sure.compat`` module
-  Introduces the modules ``sure.doubles``, ``sure.doubles.fakes``,
   ``sure.doubles.stubs`` and ``sure.doubles.dummies``
-  Sure’s featured synctactic-sugar of injecting/monkey-patching
   ``.should``, ``.should_not``, et cetera methods into
   :class:``object`` and its subclasses is disabled by default and
   needs to be enabled explicitly, programmatically via
   ``sure.enable_special_syntax()`` or via command-line with the flags:
   ``-s`` or ``--special-syntax``
-  Moves :class:``sure.original.that`` to :attr:``sure.that`` as
   an instance of :class:``sure.original.AssertionHelper`` rather
   than an alias to the class.
-  ``AssertionHelper.every_one_is()`` renamed to ``AssertionHelper.every_item_is()``


[v2.0.0]
--------

Fixed
~~~~~

-  No longer patch the builtin ``dir()`` function, which fixes pytest in
   some cases such as projects using gevent.

[v1.4.11]
---------

.. _fixed-1:

Fixed
~~~~~

-  Reading the version dinamically was causing import errors that caused
   error when installing package. Refs #144

`v1.4.7 <https://github.com/gabrielfalcao/sure/compare/1.4.6...v1.4.7>`__
-------------------------------------------------------------------------

.. _fixed-2:

Fixed
~~~~~

-  Remove wrong parens for format call. Refs #139

`v1.4.6 <https://github.com/gabrielfalcao/sure/compare/1.4.5...v1.4.6>`__
-------------------------------------------------------------------------

Added
~~~~~

-  Support and test against PyPy 3

.. _fixed-3:

Fixed
~~~~~

-  Fix safe representation in exception messages for bytes and unicode
   objects. Refs #136

`v1.4.5 <https://github.com/gabrielfalcao/sure/compare/1.4.4...v1.4.5>`__
-------------------------------------------------------------------------

.. _fixed-4:

Fixed
~~~~~

-  Correctly escape special character for ``str.format()`` for assertion
   messages. Refs #134

`v1.4.4 <https://github.com/gabrielfalcao/sure/compare/1.4.3...v1.4.4>`__
-------------------------------------------------------------------------

*Nothing to mention here.*

`v1.4.3 <https://github.com/gabrielfalcao/sure/compare/1.4.2...v1.4.3>`__
-------------------------------------------------------------------------

.. _fixed-5:

Fixed
~~~~~

-  Bug in setup.py that would break in python > 2

`v1.4.2 <https://github.com/gabrielfalcao/sure/compare/1.4.1...v1.4.2>`__
-------------------------------------------------------------------------

.. _added-1:

Added
~~~~~

-  ``ensure`` context manager to provide custom assertion messages. Refs
   #125

`v1.4.1 <https://github.com/gabrielfalcao/sure/compare/1.4.0...v1.4.1>`__
-------------------------------------------------------------------------

.. _added-2:

Added
~~~~~

-  Python 3.6 support
-  Python 3.7-dev support (allowed to fail)

.. _fixed-6:

Fixed
~~~~~

-  Do not overwrite existing class and instance attributes with sure
   properties (when. should, …). Refs #127, #129
-  Fix patched built-in ``dir()`` method. Refs #124, #128

`v1.4.0 <https://github.com/gabrielfalcao/sure/compare/1.3.0...v1.4.0>`__
-------------------------------------------------------------------------

.. _added-3:

Added
~~~~~

-  anything object which is accessible with ``sure.anything``
-  interface to extend sure. Refs #31

Removed
~~~~~~~

-  Last traces of Python 2.6 support

.. _fixed-7:

Fixed
~~~~~

-  Allow overwriting of monkey-patched properties by sure. Refs #19
-  Assertions for raises

`v1.3.0 <https://github.com/gabrielfalcao/sure/compare/1.2.9...v1.3.0>`__
-------------------------------------------------------------------------

.. _added-4:

Added
~~~~~

-  Python 3.3, 3.4 and 3.5 support
-  pypy support
-  Support comparison of OrderedDict. Refs #55

.. _fixed-8:

Fixed
~~~~~

-  ``contain`` assertion. Refs #104
