# -*- coding: utf-8 -*-
# <sure - sophisticated automated test library and runner>
# Copyright (C) <2010-2024>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import re
import time
import mock
import unittest
from collections import OrderedDict
from datetime import datetime
from datetime import timedelta
from sure import AssertionBuilder
from sure import this
from sure import within, microsecond
from sure import those
from sure import it
from sure import expects
from sure import that
from sure import assert_that
from sure import these
from sure import expect
from sure import anything


def test_4_equal_2p2():
    "this(4).should.equal(2 + 2)"

    time = datetime.now() - timedelta(0, 60)

    expect(4).should.equal(2 + 2)
    expect(time).should_not.equal(datetime.now())

    def incorrect_positive_comparison():
        expect(-33).to.equal(33)

    def incorrect_negative_expectation():
        expect(88).should_not.equal(88)

    expect(incorrect_positive_comparison).when.called.to.throw(AssertionError)
    expect(incorrect_positive_comparison).when.called.to.throw("X is -33 whereas Y is 33")

    expect(incorrect_negative_expectation).when.called.to.throw(AssertionError)
    expect(incorrect_negative_expectation).when.called.to.throw(
        "expecting 88 to be different of 88")


def test_2_within_0a2():
    "this(1).should.be.within(0, 2)"

    expect(1).should.be.within(0, 2)
    expect(4).should_not.be.within(0, 2)

    def opposite():
        expect(1).should.be.within(2, 4)

    def opposite_not():
        expect(1).should_not.be.within(0, 2)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("expects 1 to be within 2 and 4")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expects 1 to NOT be within 0 and 2")


def test_true_to_be_ok():
    "this(True).should.be.ok"

    expect(True).should.be.ok
    expect(False).should_not.be.ok

    def opposite():
        expect(False).should.be.ok

    def opposite_not():
        expect(True).should_not.be.ok

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("expects `False' to be `True'")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expects `True' to be `False'")


def test_falsy():
    "this(False).should.be.false"

    expect(False).should.be.falsy
    expect(True).should_not.be.falsy

    def opposite():
        expect(True).should.be.falsy

    def opposite_not():
        expect(False).should_not.be.falsy

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("expects `True' to be `False'")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expects `False' to be `True'")


def test_none():
    "this(None).should.be.none"

    expect(None).should.be.none
    expect(not None).should_not.be.none

    def opposite():
        expect("cool").should.be.none

    def opposite_not():
        expect(None).should_not.be.none

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("expects `cool' to be None")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expects `None' to not be None")


def test_should_be_a():
    "this(None).should.be.none"

    expect(1).should.be.an(int)
    expect([]).should.be.a('collections.abc.Iterable')
    expect({}).should_not.be.a(list)

    def opposite():
        expect(1).should_not.be.an(int)

    def opposite_not():
        expect([]).should_not.be.a('list')

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw("expects `1' to not be an `int'")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expects `[]' to not be a `list'")


def test_should_be_callable():
    "this(function).should.be.callable"

    expect(lambda: None).should.be.callable
    expect("aa").should_not.be.callable

    def opposite():
        expect("string").to.be.callable

    def opposite_not():
        expect(opposite).to_not.be.callable

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expects 'string' to be callable")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        f"expects {repr(opposite)} to not be callable"
    )


def test_iterable_should_be_empty():
    "this(iterable).should.be.empty"

    expect([]).should.be.empty
    expect([1, 2, 3]).should_not.be.empty

    def opposite():
        expect([3, 2, 1]).should.be.empty

    def opposite_not():
        expect({}).should_not.be.empty

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expects '[3, 2, 1]' to be empty but contains 3 items"
    )

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw("expects `{}' to not be empty")


def test_iterable_should_have_length_of():
    "this(iterable).should.have.length_of(N)"

    expect({'foo': 'bar', 'a': 'b'}).should.have.length_of(2)
    expect([1, 2, 3]).should_not.have.length_of(4)

    def opposite():
        expect(('foo', 'bar', 'a', 'b')).should.have.length_of(1)

    def opposite_not():
        expect([1, 2, 3]).should_not.have.length_of(3)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "the length of ('foo', 'bar', 'a', 'b') should be 1, but is 4"
    )

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "the length of [1, 2, 3] should not be 3")


def test_greater_than():
    "this(X).should.be.greater_than(Y)"

    expect(5).should.be.greater_than(4)
    expect(1).should_not.be.greater_than(2)

    def opposite():
        expect(4).should.be.greater_than(5)

    def opposite_not():
        expect(2).should_not.be.greater_than(1)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expects `4' to be greater than `5'")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "expects `2' to not be greater than `1'")


def test_greater_than_or_equal_to():
    "this(X).should.be.greater_than_or_equal_to(Y)"

    expect(4).should.be.greater_than_or_equal_to(4)
    expect(1).should_not.be.greater_than_or_equal_to(2)

    def opposite():
        expect(4).should.be.greater_than_or_equal_to(5)

    def opposite_not():
        expect(2).should_not.be.greater_than_or_equal_to(1)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expects `4' to be greater than or equal to `5'")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "expects `2' to not be greater than or equal to `1'")


def test_lower_than():
    "this(X).should.be.lower_than(Y)"

    expect(4).should.be.lower_than(5)
    expect(2).should_not.be.lower_than(1)

    def opposite():
        expect(5).should.be.lower_than(4)

    def opposite_not():
        expect(1).should_not.be.lower_than(2)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expects `5' to be lower than `4'")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "expects `1' to not be lower than `2'")


def test_lower_than_or_equal_to():
    "this(X).should.be.lower_than_or_equal_to(Y)"

    expect(5).should.be.lower_than_or_equal_to(5)
    expect(2).should_not.be.lower_than_or_equal_to(1)

    def opposite():
        expect(5).should.be.lower_than_or_equal_to(4)

    def opposite_not():
        expect(1).should_not.be.lower_than_or_equal_to(2)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "expects `5' to be lower than or equal to `4'")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "expects `1' to not be lower than or equal to `2'")


def test_assertion_builder_be__call__():
    "this(ACTUAL).should.be(EXPECTED) where ACTUAL and EXPECTED are evaluated as identical in Python"

    d1 = {}
    d2 = d1
    d3 = {}

    assert isinstance(this(d2).should.be(d1), bool)
    expect(d2).should.be(d1)
    expect(d3).should_not.be(d1)

    def wrong_should():
        return this(d3).should.be(d1)

    def wrong_should_not():
        return this(d2).should_not.be(d1)

    expect(wrong_should_not).when.called.should.throw(
        AssertionError,
        '{} should not be the same object as {}',
    )
    expect(wrong_should).when.called.should.throw(
        AssertionError,
        '{} should be the same object as {}',
    )


def test_have_property():
    "this(instance).should.have.property(property_name)"

    class ChemicalElement(object):
        name = "Uranium"

        def __repr__(self):
            return f"<ChemicalElement name={repr(self.name)}>"

    chemical_element = ChemicalElement()

    expect(chemical_element).should.have.property("name")
    expect(chemical_element).should_not.have.property("mass")

    def opposite():
        expect(chemical_element).should_not.have.property("name")

    def opposite_not():
        expect(chemical_element).should.have.property("mass")

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "<ChemicalElement name='Uranium'> should not have the property `name' which is actually present and holds the value `Uranium'"
    )

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "<ChemicalElement name='Uranium'> should have the property `mass' which is not present"
    )


def test_have_property_with_value():
    ("this(instance).should.have.property(property_name).being or "
     ".with_value should allow chain up")

    class ChemicalElement(object):
        name = "Uranium"

        def __repr__(self):
            return f"<ChemicalElement name={repr(self.name)}>"

    chemical_element = ChemicalElement()

    expect(chemical_element).should.have.property("name").being.equal("Uranium")
    expect(chemical_element).should.have.property("name").not_being.equal("Foo")

    def opposite():
        expect(chemical_element).should.have.property("name").not_being.equal(
            "Uranium")

    def opposite_not():
        expect(chemical_element).should.have.property("name").being.equal(
            "Foo")

    expect(opposite).when.called.to.throw(
        AssertionError,
        "expecting 'Uranium' to be different of 'Uranium'"
    )

    expect(opposite_not).when.called.to.throw(
        AssertionError,
        "X is 'Uranium' whereas Y is 'Foo'"
    )


def test_have_key():
    "this(dictionary).should.have.key(key_data)"

    data_structure = {'data': "binary blob"}

    expect(data_structure).should.have.key("data")
    expect(data_structure).should_not.have.key("mass")

    def opposite():
        expect(data_structure).should_not.have.key("data")

    def opposite_not():
        expect(data_structure).should.have.key("mass")

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "{'data': 'binary blob'} should not have the key `data' "
        "which is actually present and holds the value `binary blob'"
    )

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "{'data': 'binary blob'} should have the key `mass' which is not present"
    )


def test_have_key_with_value():
    ("this(dictionary).should.have.key(key_name).being or "
     ".with_value should allow chain up")

    chemical_element = dict(name="Uranium")

    expect(chemical_element).should.have.key("name").being.equal("Uranium")
    expect(chemical_element).should.have.key("name").not_being.equal("Foo")

    def opposite():
        expect(chemical_element).should.have.key("name").not_being.equal(
            "Uranium"
        )

    def opposite_not():
        expect(chemical_element).should.have.key("name").being.equal(
            "Foo"
        )

    expect(opposite).when.called.to.throw(
        AssertionError,
        "'Uranium' to be different of 'Uranium'"
    )

    expect(opposite_not).when.called.to.throw(
        AssertionError,
        "X is 'Uranium' whereas Y is 'Foo'"
    )


def test_look_like():
    "this('   aa  \n  ').should.look_like('aa')"

    expect('   \n  aa \n  ').should.look_like('AA')
    expect('   \n  bb \n  ').should_not.look_like('aa')

    def opposite():
        expect('\n aa \n').should.look_like('bb')

    def opposite_not():
        expect('\n aa \n').should_not.look_like('aa')

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(r"'\n aa \n' does not look like 'bb'")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(r"'\n aa \n' should not look like 'aa' but does")


def test_equal_with_repr_of_complex_types_and_unicode():
    "test usage of repr() inside expect(complex1).to.equal(complex2)"

    class Y(object):
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            return self.x

        def __eq__(self, other):
            return self.x == other.x

    y1 = dict(
        G=1,
        O=Y('Gabriel Falcão'),
        T='skills',
    )

    expect(y1).to.equal(dict(
        G=1,
        O=Y('Gabriel Falcão'),
        T='skills',
    ))


def test_equal_with_repr_of_complex_types_and_repr():
    "test usage of repr() inside expect(complex1).to.equal(complex2)"

    class Y(object):
        def __init__(self, x):
            self.x = x

        def __repr__(self):
            return self.x

        def __eq__(self, other):
            return self.x == other.x

    y1 = {
        'G': 1,
        'O': Y('Gabriel Falcão'),
        'T': 'skills',
    }

    expect(y1).to.equal({
        'G': 1,
        'O': Y('Gabriel Falcão'),
        'T': 'skills',
    })

    expect(y1).to_not.equal({
        'G': 1,
        'O': Y('Gabriel Falçao'),
        'T': 'skills',
    })

    def opposite():
        expect(y1).to.equal({
            'G': 1,
            'O': Y('Gabriel Falçao'),
            'T': 'skills',
        })

    def opposite_not():
        expect(y1).to_not.equal({
            'G': 1,
            'O': Y('Gabriel Falcão'),
            'T': 'skills',
        })

    expect(opposite).when.called.to.throw(
        AssertionError,
        "X['O'] != Y['O']"
    )

    expect(opposite_not).when.called.to.throw(
        AssertionError,
        "expecting {'G': 1, 'O': Gabriel Falcão, 'T': 'skills'} to be different of {'G': 1, 'O': Gabriel Falcão, 'T': 'skills'}"
    )


def test_match_regex():
    "expect('some string').to.match(r'\\w{4} \\w{6}') matches regex"

    expect("some string").should.match(r"\w{4} \w{6}")
    expect("some string").should_not.match(r"^\d*$")

    def opposite():
        expect("some string").should.match(r"\d{2} \d{4}")

    def opposite_not():
        expect("some string").should_not.match(r"some string")

    expect(opposite).when.called.to.throw(
        AssertionError,
        "'some string' doesn't match the regular expression /\d{2} \d{4}/")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "'some string' should not match the regular expression /some string/")


def test_match_contain():
    "expect('some string').to.contain('tri')"

    expect("some string").to.contain("tri")
    expect("some string").to_not.contain('foo')

    def opposite():
        expect("some string").should.contain("bar")

    def opposite_not():
        expect("some string").should_not.contain(r"string")

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw(
        "`bar' should be in `some string'")

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw(
        "`string' should not be in `some string'")


def test_catching_exceptions():
    # Given that I have a function that raises an exceptiont that does
    # *not* inherit from :exc:`Exception'
    def function():
        raise SystemExit(2)

    # When I call it testing which exception it's raising, Then it should be
    # successful
    expect(function).when.called_with().should.throw(SystemExit)


def test_catching_exceptions_with_params():
    # Given that I have a function that raises an exceptiont that does
    # *not* inherit from :exc:Exception
    def function(foo):
        raise SystemExit(2)

    # When I call it testing which exception it's raising, Then it should be
    # successful
    expect(function).when.called_with(0).should.throw(SystemExit)


def test_success_with_params():
    def function(foo):
        pass

    expect(function).when.called_with(0).should_not.throw(TypeError)


def test_success_with_params_exception():
    def function():
        pass

    expect(function).when.called_with(0).should.throw(TypeError)


def test_throw_matching_regex():
    def function(num):
        if num == 1:
            msg = 'this message'
        else:
            msg = 'another thing'

        raise ValueError(msg)

    expect(function).when.called_with(1).to.throw(ValueError, 'this message')
    expect(function).when.called_with(1).to.throw(re.compile(r'(this message|another thing)'))
    expect(function).when.called_with(2).to.throw(ValueError, 'another thing')
    expect(function).when.called_with(2).to.throw(ValueError, re.compile(r'(this message|another thing)'))

    try:
        expect(function).when.called_with(1).should.throw(re.compile(r'invalid regex'))
        raise RuntimeError('should not have reached here')

    except AssertionError as e:
        expect(str(e)).to.equal("When calling 'function [tests/test_assertion_builder.py line 632]' the exception message does not match. Expected to match regex: 'invalid regex'\n against:\n 'this message'")

    try:
        expect(function).when.called_with(1).should.throw(ValueError, re.compile(r'invalid regex'))
        raise RuntimeError('should not have reached here')
    except AssertionError as e:
        expect(str(e)).to.equal("When calling 'function [tests/test_assertion_builder.py line 632]' the exception message does not match. Expected to match regex: 'invalid regex'\n against:\n 'this message'")


def test_should_not_be_different():
    "'something'.should_not.be.different('SOMETHING'.lower())"

    part1 = '''<root>
  <a-tag with-attribute="one">AND A VALUE</a-tag>
</root>'''

    part2 = '''<root>
  <a-tag with-attribute="two">AND A VALUE</a-tag>
</root>'''

    expect(part1).should.be.different_of(part2)
    expect(part2).should_not.be.different_of(part2)

    def opposite():
        expect(part2).should.be.different_of(part2)

    def opposite_not():
        expect(part1).should_not.be.different_of(part2)

    expect(opposite).when.called.to.throw(AssertionError)
    expect(opposite).when.called.to.throw('''<root>
  <a-tag with-attribute="two">AND A VALUE</a-tag>
</root> should be different of <root>
  <a-tag with-attribute="two">AND A VALUE</a-tag>
</root>''')

    expect(opposite_not).when.called.to.throw(AssertionError)
    expect(opposite_not).when.called.to.throw('''Difference:

  <root>
-   <a-tag with-attribute="one">AND A VALUE</a-tag>
?                           --
+   <a-tag with-attribute="two">AND A VALUE</a-tag>
?                          ++
  </root>''')


def test_equals_handles_mock_mock_call_list():
    ".equal() Should convert :mod:`mock._CallList` instances to lists"

    # Given the following mocked callback
    callback = mock.Mock()

    # When I call the callback with a few parameters twice
    callback(a=1, b=2)
    callback(a=3, b=4)

    # Then I see I can compare the call list without manually
    # converting anything

    expect(callback.call_args_list).should.equal([
        mock.call(a=1, b=2),
        mock.call(a=3, b=4),
    ])


def test_equals_handles_unittest_mock_call_list():
    ".equal() Should convert :mod:`unittest.mock._CallList` instances to lists"

    # Given the following mocked callback
    callback = unittest.mock.Mock()

    # When I call the callback with a few parameters twice
    callback(a=1, b=2)
    callback(a=3, b=4)

    # Then I see I can compare the call list without manually
    # converting anything

    expect(callback.call_args_list).should.equal(unittest.mock._CallList([
        mock.call(a=1, b=2),
        mock.call(a=3, b=4),
    ]))


def test_equals_handles_float_with_epsilon():
    ".equal(what, epsilon=XXX) should check for equality with an epsilon for float values"
    float1 = 4.242423
    float2 = 4.242420

    expect(float1).should_not.be.equal(float2)
    expect(float1).should.be.equal(float2, epsilon=0.000005)

    float_list1 = [4.242421, 4.242422, 4.242423, 4.242424, 4.242425]
    float_list2 = [4.242420, 4.242420, 4.242420, 4.242420, 4.242420]

    expect(float_list1).should_not.be.equal(float_list2)
    expect(float_list1).should.be.equal(float_list2, epsilon=0.000005)

    float_dict1 = {"f1": 4.242421, "f2": 4.242422, "f3": 4.242423, "f4": 4.242424, "f5": 4.242425}
    float_dict2 = {"f1": 4.242420, "f2": 4.242420, "f3": 4.242420, "f4": 4.242420, "f5": 4.242420}

    expect(float_dict1).should_not.be.equal(float_dict2)
    expect(float_dict1).should.be.equal(float_dict2, epsilon=0.000005)


def test_equals_dictionaries_with_tuple_keys():
    ('.equal() with dict containing tuples as keys should work')

    X = {
        ("0.0.0.0", 3478): "chuck norris",
    }

    Y = {
        ("0.0.0.0", 400): "chuck norris",
    }

    expect(X).should_not.equal(Y)
    expect(Y).should_not.equal(X)


def test_ordereddict_comparison():
    ".equal(OrderedDict) should check if two ordered dicts are the same"
    result = {
        "fields": OrderedDict([
            ("name", "Helium"),
            ("mass", "4.002602"),
        ]),
        "unused": OrderedDict([]),
    }

    expectation = {
        "fields": OrderedDict([
            ("name", "Helium"),
            ("mass", "4.002602"),
        ]),
        "unused": OrderedDict([]),
    }

    expect(result).should.equal(expectation)


def test_ordereddict_comparison_differing_order():
    ".equal(OrderedDict) should raise error when on differing order"
    result = {
        "fields": OrderedDict([
            ("mass", "4.002602"),
            ("name", "Helium"),
        ]),
        "unused": OrderedDict([]),
    }

    expectation = {
        "fields": OrderedDict([
            ("name", "Helium"),
            ("mass", "4.002602"),
        ]),
        "unused": OrderedDict([]),
    }

    expects(expect(result).should.equal).when.called_with(expectation).to.have.raised(
        AssertionError,
        "X['fields'] and Y['fields'] appear have keys in different order"
    )


def test_equals_anything():
    val = 1
    expect(val).to.be.equal(anything)

    val = {'key': 1, 'other_key': 4}
    expect(val).to.be.equal({'key': 1, 'other_key': anything})

    val = {'key': 1, 'other_key': 'yo!'}
    expect(val).to.be.equal({'key': 1, 'other_key': anything})

    val = [1, 2, 3, 4]
    expect(val).to.be.equal([1, anything, 3, anything])


def test_equals_crosstype():
    class MyFloat(float):
        pass
    expect(MyFloat(3.33)).to.be.equal(3.33)


def test_assertion_builder_variants():
    """'this', 'those', 'it', 'expects', 'that', 'assert_that',
    'these' and 'expect' should be instances of the AssertionBuilder class"""

    assert isinstance(it, AssertionBuilder)
    assert isinstance(this, AssertionBuilder)
    assert isinstance(these, AssertionBuilder)
    assert isinstance(those, AssertionBuilder)
    assert isinstance(that, AssertionBuilder)
    assert isinstance(expect, AssertionBuilder)
    assert isinstance(expects, AssertionBuilder)
    assert isinstance(assert_that, AssertionBuilder)


def test_within_time():
    "@sure.within() decorator should raise error if the decorated function takes longer than the amount of time specified through its keyword-argument DSL"

    @within(one=microsecond)
    def test():
        time.sleep(0.1)

    def trigger():
        test()

    expects(trigger).when.called.to.have.raised(
        AssertionError,
        "test [tests/test_assertion_builder.py line 853] did not run within one microseconds"
    )
