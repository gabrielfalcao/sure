## #!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from six import  PY2

from sure import expect
from sure.core import safe_repr
from sure.compat import compat_repr


def test_basic_list():
    "safe_repr should display a simple list"
    X = ['one', 'yeah']
    expect(safe_repr(X)).should.equal(compat_repr(
        "['one', 'yeah']"
    ))


def test_basic_dict():
    "safe_repr should return a sorted repr"
    X = {'b': 'd', 'a': 'c'}
    expect(safe_repr(X)).should.equal(compat_repr(
        "{'a': 'c', 'b': 'd'}"
    ))


def test_nested_dict():
    "dicts nested inside values should also get sorted"
    X = {'my::all_users': [{'age': 33, 'name': 'John', 'foo': 'bar'}]}
    expect(safe_repr(X)).should.equal(compat_repr(
        '''{'my::all_users': [{'age': 33, 'foo': 'bar', 'name': 'John'}]}'''
    ))


def test_unicode():
    "dicts with unicode should work properly"
    class Y(object):
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            if PY2:
                # PY2 should return the regular (unicode) string
                return self.x.encode('utf-8')
            else:
                return self.x

        def __eq__(self, other):
            return self.x == other.x

    y1 = {
        'a': 2,
        'b': Y('Gabriel Falcão'),
        'c': 'Foo',
    }
    name = 'Gabriel Falc\xe3o' if PY2 else 'Gabriel Falcão'

    expect(safe_repr(y1)).should.equal(compat_repr(
        "{'a': 2, 'b': %s, 'c': 'Foo'}" % name
    ))
