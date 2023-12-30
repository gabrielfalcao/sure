"""This module provides a limited set of "test-doubles"

The concept of "test-double" employed in the module :py:mod:`sure.doubles` is imperative to, inspired or derived from the Martin Fowler's great article `"Mocks Aren't Stubs" <https://martinfowler.com/articles/mocksArentStubs.html>`_.

To that extent, it currently presents the following sub-modules:

- :py:mod:`sure.doubles.fakes`
- :py:mod:`sure.doubles.stubs`

The other kinds of test-doubles appearing in the aforementioned
article - namely: Dummies, Spies and Mocks - are not at all
officially provided or supported by :py:mod:`sure`.

In the very specific case of the kind of test-doubles referred to as
"Mocks", the author of :py:mod:`sure` loosely recommends the usage of Python's
builtin :py:mod:`unittest.mock` and its underlying components with the
added caveat that, at the time of this writing,
:py:class:`~unittest.mock.Mock` and its related module components
provide kinds of features that seem to reasonably cover all or almost
all the features expected from all distinct types of test-doubles
while not making a reasonably clear distinction or articulation
between the peculiarities that bring value to that otherwise clear
distinction.

The value in case lies - primarily but not limited to - somewhere
within the principles - along with related disciplines and practices -
of "Separation of concerns" and "Didactics". This is because an
unclear distinction between the aforementioned kinds of test-doubles
leaves room for misinterpretation of rather important concepts
underlying each kind, and because it is apparent that students of the
discipline of Automated Software Testing in Python facing the sorts of
obstacles that eventually lead to the discovery of the concept of
"Mocks" and consequently or inconsequently ends up using the
:py:mod:`unittest.mock` often miss the opportunity of understanding
the real tangible value in doing so the "right" way.

To conclude, the author of :py:mod:`sure` strongly recommends the
reader to go to the `Fowler's article covering those distinctions
<https://martinfowler.com/articles/mocksArentStubs.html>`_ if you have
not already seriously done just that yet.
"""
from sure.doubles.fakes import FakeOrderedDict
from sure.doubles.stubs import stub

__all__ = ['FakeOrderedDict', 'stub']
