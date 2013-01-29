## #!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from sure import expect
from sure.core import safe_repr
from sure.six import compat_repr, PY3


def test_basic_list():
    "safe_repr should display a simple list"
    X = [u'one', u'yeah']
    expect(safe_repr(X)).should.equal(compat_repr(
        "['one', 'yeah']"
    ))


def test_basic_dict():
    "safe_repr should return a sorted repr"
    X = {u'b': u'd', u'a': u'c'}
    expect(safe_repr(X)).should.equal(compat_repr(
        "{'a': 'c', 'b': 'd'}"
    ))


def test_nested_dict():
    "dicts nested inside values should also get sorted"
    X = {u'my::all_users': [{u'age': 33, u'name': u'John', u'foo': u'bar'}]}
    expect(safe_repr(X)).should.equal(compat_repr(
        '''{'my::all_users': [{'age': 33, 'foo': 'bar', 'name': 'John'}]}'''
    ))


def test_unicode():
    "dicts with unicode should work properly"
    class Y(object):
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            if PY3:
                # PY3K should return the regular (unicode) string
                return self.x
            else:
                return self.x.encode('utf-8')

        def __eq__(self, other):
            return self.x == other.x

    y1 = {
        'a': 2,
        'b': Y(u'Gabriel Falcão'),
        'c': u'Foo',
    }
    name = u'Gabriel Falcão' if PY3 else u'Gabriel Falc\xe3o'

    expect(safe_repr(y1)).should.equal(compat_repr(
        "{'a': 2, 'b': %s, 'c': 'Foo'}" % name
    ))
