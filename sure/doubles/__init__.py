"""This module provides a limited set of "test-doubles"

The concept of "test-double" employed in the module :mod:`sure.doubles` is imperative to, inspired or derived from the Martin Fowler's great article `"Mocks Aren't Stubs" <https://martinfowler.com/articles/mocksArentStubs.html>`_.

To that extent, it currently presents the following sub-modules:

- :mod:`sure.doubles.dummies`
- :mod:`sure.doubles.fakes`
- :mod:`sure.doubles.stubs`

Considering the aforementioned `article <https://martinfowler.com/articles/mocksArentStubs.html>`_, there are two types of
test-doubles missing from the list above: "spies" and "mocks". That is
because neither of those are presently provided in :mod:`sure` as
test-doubles.

In the very specific case of the type of test-doubles referred to as
"Mocks", :mod:`sure` loosely recommends the usage of Python's builtin
:mod:`mock` and its underlying components with the added caveat that,
at the time of this writing, :class:`~mock.Mock` and its related
module components provide types of features that seem to reasonably
cover all or almost all the features expected from all distinct types
of test-doubles while not making a reasonably clear distinction or
articulation between the peculiarities that bring value to that
otherwise clear distinction.

The value in case lies - primarily but not limited to - somewhere
within the principles, related disciplines or practices of "Separation
of concerns" and "Didactics". This is because an unclear distinction
between the aforementioned types of test-doubles leaves room for
misinterpretation of rather important concepts underlying each type,
and because it is apparent that students of the discipline of
Automated Software Testing in Python facing the sorts of obstacles
that eventually lead to the discovery of the concept of "Mocks" and
consequently stumble upon the :mod:`mock` module often fail to realize
the values of a thorough and clear understanding of the concept of
"test-doubles" both in terms of theory and practice, as well as the
surmounting costs of writing inconcise, liable tests that generate
unwarranted tech-debt.

To conclude, the :mod:`mock` and its components have, in some sense,
quite intelligent internal mechanisms that can prove quite powerful at
virtually every occasion. Nevertheless wielding intelligent tools
should ideally require a level of care for knowledge that, more often
than not, can only be achieved by those who take the enterprise of
intellectual pursuit seriously and not insincerely, and continuously
seek to hone their software-craftsmanship skills.

`Fowler's article
<https://martinfowler.com/articles/mocksArentStubs.html>`_ is great
source of knowledge to dispel the sorts of harmful misconceptions made
salient in this section.
"""

from sure.doubles.fakes import FakeOrderedDict
from sure.doubles.stubs import stub
from sure.doubles.dummies import anything, Dummy, AnythingOfType, anything_of_type

__all__ = ['FakeOrderedDict', 'stub', 'anything', 'Dummy', 'AnythingOfType', 'anything_of_type']
