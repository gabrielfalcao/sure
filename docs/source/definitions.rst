.. _Definitions:

Definitions
===========

This section defines terms used across :ref:`Sure`'s documentation,
code and run-time error messages and must be interpreted accordingly
as to prevent confusion, misunderstanding and abuse of any manner,
form or kind be it real or virtual.

Each term is defined in the subsections below which are titled by the
term itself and followed by the actual definition of the term in case
which shall be entirely comprehended as they appear typographically
written regardless of capitalization. Synonyms may be presented within
each of those sections.

These terms might be updated in the event of emerging incorrectness or
general evolution of the :ref:`Sure` project.


.. _truthy:

truthy
------

Defines Python objects whose logical value is equivalent to the
boolean value of ``True``.

More specifically, any valid Python code evaluted by :class:`bool` as
``True`` might appear written as ``truthy`` within the scope of
:ref:`Sure`.

Synonyms: ``true``, ``truthy``, ``ok``


.. _falsy:

falsy
-----

Defines Python objects whose logical value is equivalent to the
boolean value of ``False``.

More specifically, any valid Python code evaluted by :class:`bool` as
``False`` might appear written as ``falsy`` within the scope of
:ref:`Sure`.

Synonyms: ``false``, ``falsy``, ``not_ok``


.. _none:

none
----

Defines Python objects whose logical value is equivalent to the
boolean value of ``False``.

Synonyms: ``none``, ``None``


.. _special syntax definition:

special syntax
--------------

:ref:`Special Syntax` refers to the unique feature of giving *special
properties* to every in-memory Python :class:`python:object` from
which to build assertions.

Such special properties are semantically divided in two categories:
:ref:`positive <positive assertion properties>` (``do``, ``does``,  ``must``, ``should``,  ``when``) and :ref:`negative
<negative assertion properties>` (``do_not``, ``dont``, ``does_not``, ``doesnt``, ``must_not``, ``mustnt``, ``should_not``, ``shouldnt``).
