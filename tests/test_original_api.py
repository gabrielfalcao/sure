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
import os
import sure
import time

from datetime import datetime

from sure import that, this
from sure import expects
from sure import action_for
from sure import scenario
from sure import within
from sure import second, miliseconds
from sure import StagingArea
from sure.errors import WrongUsageError
from sure.special import is_cpython
from sure.loader import collapse_path
from sure.original import all_integers


def test_setup_with_context():
    "sure.with_context() runs setup before the function itself"

    def setup(context):
        context.name = None

    @sure.that_with_context(setup)
    def variable_is_within_context(context):
        assert isinstance(context, StagingArea)
        assert hasattr(context, "name")

    variable_is_within_context()
    expects(variable_is_within_context.__name__).to.equal(
        "variable_is_within_context",
    )


def test_context_of_sure_that_with_context_decorated_functions_is_not_optional():
    "sure.that_with_context() when no context is given it fails"

    def setup(context):
        pass

    @sure.that_with_context(setup)
    def it_crashes():
        assert True

    assert that(it_crashes).raises(
        TypeError,
        (
            "the function it_crashes defined at tests/test_original_api.py line 60, is being "
            "decorated by either @that_with_context or @scenario, so it should "
            "take at least 1 parameter, which is the test context"
        ),
    )


def test_setup_with_context_context_failing():
    "sure.that_with_context() in a failing test"

    def setup(context):
        context.name = None

    @sure.that_with_context(setup)
    def function(context):
        assert False, "should fail with this exception"

    assert that(function).raises("should fail with this exception")


def test_teardown_with_context():
    "sure.with_context() runs teardown before the function itself"

    class data_structure:
        pass

    def setup(context):
        data_structure.modified = True

    def teardown(context):
        del data_structure.modified

    @sure.that_with_context(setup, teardown)
    def data_structure_was_modified(context):
        assert hasattr(data_structure, "modified")
        assert data_structure.modified

    data_structure_was_modified()
    assert not hasattr(data_structure, "modified")


def test_that_is_a():
    "that() is_a(object)"

    data_structure = "data_structure"

    assert that(data_structure).is_a(str)
    assert isinstance(data_structure, str)


def test_that_equals():
    "that() equals(string)"

    data_structure = "data_structure"

    assert that("data_structure").equals(data_structure)
    assert data_structure == "data_structure"


def test_that_differs():
    "that() differs(object)"

    data_structure = "data_structure"

    assert that(data_structure).differs("23123%FYTUGIHOfdf")
    assert data_structure != "23123%FYTUGIHOfdf"


def test_that_has():
    "that() has(object)"

    class Class:
        value = "some class"

    Object = Class()
    dictionary = {
        "value": "Value",
    }
    value = "value"

    assert hasattr(Class, "value")
    expects(Class).has("value")
    expects(Class).to.be.like("value")
    assert "value" in that(Class)

    assert hasattr(Object, "value")
    expects(Object).has("value")
    expects(Object).to.be.like("value")
    assert "value" in that(Object)

    assert "value" in dictionary
    expects(dictionary).has("value")
    expects(dictionary).to.be.like("value")
    assert "value" in that(dictionary)

    expects(value).has("value")
    expects(value).to.be.like("value")
    assert "value" in that(value)
    expects(value).has("va")
    expects(value).to.be.like("va")
    assert "val" in that(value)
    expects(value).has("val")
    expects(value).to.be.like("ue")
    assert "ue" in that(value)


def test_that_at_key_equals():
    "that().at(object).equals(object)"

    class Class:
        attribute = "some class"

    Object = Class()
    dictionary = {
        "attribute": "data_structure",
    }

    assert that(Class).at("attribute").equals("some class")
    assert that(Object).at("attribute").equals("some class")
    assert that(dictionary).at("attribute").equals("data_structure")


def test_that_len_is():
    "that() len_is(number)"

    lst = range(1000)

    assert that(lst).len_is(1000)
    assert len(lst) == 1000
    assert that(lst).len_is(lst)


def test_that_len_greater_than():
    "that() len_greater_than(number)"

    lst = range(1000)
    lst2 = range(100)

    assert that(lst).len_greater_than(100)
    assert len(lst) == 1000
    assert that(lst).len_greater_than(lst2)


def test_that_len_greater_than_should_raise_assertion_error():
    "that() len_greater_than(number) raise AssertionError"

    lst = list(range(1000))
    try:
        that(lst).len_greater_than(1000)
    except AssertionError as e:
        expects(str(e)).to.equal(
            "the length of the list should be greater then %d, but is %d" % (1000, 1000)
        )


def test_that_len_greater_than_or_equals():
    "that() len_greater_than_or_equals(number)"

    lst = list(range(1000))
    lst2 = list(range(100))

    assert that(lst).len_greater_than_or_equals(100)
    assert that(lst).len_greater_than_or_equals(1000)
    assert len(lst) == 1000
    assert that(lst).len_greater_than_or_equals(lst2)
    assert that(lst).len_greater_than_or_equals(lst)


def test_that_len_greater_than_or_equals_should_raise_assertion_error():
    "that() len_greater_than_or_equals(number) raise AssertionError"

    lst = list(range(1000))
    try:
        that(lst).len_greater_than_or_equals(1001)
    except AssertionError as e:
        expects(str(e)).to.equal(
            "the length of %r should be greater then or equals %d, but is %d"
            % (lst, 1001, 1000)
        )


def test_that_len_lower_than():
    "that() len_lower_than(number)"

    lst = list(range(100))
    lst2 = list(range(1000))

    assert that(lst).len_lower_than(101)
    assert len(lst) == 100
    assert that(lst).len_lower_than(lst2)


def test_that_len_lower_than_should_raise_assertion_error():
    "that() len_lower_than(number) raise AssertionError"

    lst = list(range(1000))
    try:
        that(lst).len_lower_than(1000)
    except AssertionError as e:
        expects(str(e)).to.equal(
            "the length of %r should be lower then %d, but is %d" % (lst, 1000, 1000)
        )


def test_that_len_lower_than_or_equals():
    "that() len_lower_than_or_equals(number)"

    lst = list(range(1000))
    lst2 = list(range(1001))

    assert that(lst).len_lower_than_or_equals(1001)
    assert that(lst).len_lower_than_or_equals(1000)
    assert len(lst) == 1000
    assert that(lst).len_lower_than_or_equals(lst2)
    assert that(lst).len_lower_than_or_equals(lst)


def test_that_len_lower_than_or_equals_should_raise_assertion_error():
    "that() len_lower_than_or_equals(number) raise AssertionError"

    lst = list(range(1000))

    try:
        that(lst).len_lower_than_or_equals(100)
    except AssertionError as e:
        expects(str(e)).to.equal(
            "the length of %r should be lower then or equals %d, but is %d"
            % (lst, 100, 1000)
        )


def test_that_checking_all_atributes():
    "that(iterable).the_attribute('name').equals('value')"

    class shape(object):
        def __init__(self, name):
            self.kind = "geometrical form"
            self.name = name

    shapes = [
        shape("circle"),
        shape("square"),
        shape("rectangle"),
        shape("triangle"),
    ]

    assert that(shapes).the_attribute("kind").equals("geometrical form")


def test_that_checking_all_atributes_of_range():
    "that(iterable, within_range=(1, 2)).the_attribute('name').equals('value')"

    class shape(object):
        def __init__(self, name):
            self.kind = "geometrical form"
            self.name = name

        def __repr__(self):
            return "<%s:%s>" % (self.kind, self.name)

    shapes = [
        shape("circle"),
        shape("square"),
        shape("square"),
        shape("triangle"),
    ]

    assert shapes[0].name != "square"
    assert shapes[3].name != "square"

    assert shapes[1].name == "square"
    assert shapes[2].name == "square"

    assert that(shapes, within_range=(1, 2)).the_attribute("name").equals("square")


def test_that_checking_all_elements():
    "that(iterable).every_item_is('value')"
    shapes = [
        "cube",
        "ball",
        "ball",
        "piramid",
    ]

    assert shapes[0] != "ball"
    assert shapes[3] != "ball"

    assert shapes[1] == "ball"
    assert shapes[2] == "ball"

    assert that(shapes, within_range=(1, 2)).every_item_is("ball")


def test_that_checking_each_matches():
    "that(iterable).in_each('').equals('value')"

    class animal(object):
        def __init__(self, kind):
            self.attributes = {
                "class": "mammal",
                "kind": kind,
            }

    animals = [
        animal("dog"),
        animal("cat"),
        animal("cow"),
        animal("cow"),
        animal("cow"),
    ]

    assert animals[0].attributes["kind"] != "cow"
    assert animals[1].attributes["kind"] != "cow"

    assert animals[2].attributes["kind"] == "cow"
    assert animals[3].attributes["kind"] == "cow"
    assert animals[4].attributes["kind"] == "cow"

    assert animals[0].attributes["class"] == "mammal"
    assert animals[1].attributes["class"] == "mammal"
    assert animals[2].attributes["class"] == "mammal"
    assert animals[3].attributes["class"] == "mammal"
    assert animals[4].attributes["class"] == "mammal"

    assert that(animals).in_each("attributes['class']").matches("mammal")
    assert (
        that(animals)
        .in_each("attributes['class']")
        .matches(["mammal", "mammal", "mammal", "mammal", "mammal"])
    )

    assert (
        that(animals)
        .in_each("attributes['kind']")
        .matches(["dog", "cat", "cow", "cow", "cow"])
    )

    try:
        assert that(animals).in_each("attributes['kind']").matches(["dog"])
        assert False, "should not reach here"
    except AssertionError as e:
        assert that(str(e)).equals(
            "%r has 5 items, but the matching list has 1: %r"
            % (
                ["dog", "cat", "cow", "cow", "cow"],
                ["dog"],
            )
        )


def test_that_raises():
    "that(callable, with_args=[arg1], and_kws={'arg2': 'value'}).raises(SomeException)"
    global called

    called = False

    def function(arg1=None, arg2=None):
        global called
        called = True
        if arg1 == 1 and arg2 == 2:
            raise RuntimeError("yeah, it failed")

        return "OK"

    try:
        function(1, 2)
        assert False, "should not reach here"

    except RuntimeError as e:
        assert str(e) == "yeah, it failed"

    except Exception:
        assert False, "should not reach here"

    finally:
        assert called
        called = False

    called = False
    expects(function(3, 5)).to.equal("OK")
    assert called

    called = False
    assert that(function, with_args=[1], and_kws={"arg2": 2}).raises(RuntimeError)
    assert called

    called = False
    assert that(function, with_args=[1], and_kws={"arg2": 2}).raises(
        RuntimeError, "yeah, it failed"
    )
    assert called

    called = False
    assert that(function, with_args=[1], and_kws={"arg2": 2}).raises(
        "yeah, it failed"
    )
    assert called

    called = False
    assert that(function, with_kws={"arg1": 1, "arg2": 2}).raises(RuntimeError)
    assert called

    called = False
    assert that(function, with_kws={"arg1": 1, "arg2": 2}).raises(
        RuntimeError, "yeah, it failed"
    )
    assert called

    called = False
    assert that(function, with_kws={"arg1": 1, "arg2": 2}).raises("yeah, it failed")
    assert called

    called = False
    assert that(function, with_kws={"arg1": 1, "arg2": 2}).raises(r"it fail")
    assert called

    called = False
    assert that(function, with_kws={"arg1": 1, "arg2": 2}).raises(
        RuntimeError, r"it fail"
    )
    assert called


def test_that_looks_like():
    "that('String\\n with BREAKLINE').looks_like('string with breakline')"
    assert that("String\n with BREAKLINE").looks_like("string with breakline")


def test_that_raises_does_raise_for_exception_type_mismatch():
    "that(callable(RuntimeError)).raises(TypeError)"

    error = r".*should raise <class .*FooError.*, but raised <class .*BarError.*"

    class FooError(Exception):
        pass

    class BarError(Exception):
        pass

    def my_function():
        raise BarError("OOps")

    try:
        assert that(my_function).raises(FooError, "OOps")
        assert False, "should never reach here"
    except AssertionError as e:
        import re

        assert re.match(error, str(e))


def test_that_raises_with_args():
    "that(callable, with_args=['foo']).raises(FooError)"

    class FooError(Exception):
        pass

    def my_function(string):
        if string == "foo":
            raise FooError("OOps")

    assert that(my_function, with_args=["foo"]).raises(FooError, "OOps")


def test_that_does_not_raise_with_args():
    "that(callable).doesnt_raise(FooError) and does_not_raise"

    class FooError(Exception):
        pass

    def my_function(string):
        if string == "foo":
            raise FooError("OOps")

    assert that(my_function, with_args=["foo"]).raises(FooError, "OOps")


def test_that_contains_string():
    "that('foobar').contains('foo')"

    assert "foo" in "foobar"
    assert that("foobar").contains("foo")


def test_that_doesnt_contain_string():
    "that('foobar').does_not_contain('123'), .doesnt_contain"

    assert "123" not in "foobar"
    assert that("foobar").doesnt_contain("123")
    assert that("foobar").does_not_contain("123")


def test_that_contains_none():
    "that('foobar').contains(None)"

    def assertions():
        assert that("foobar").contains(None)

    error_msg = (
        "'in <string>' requires string as left operand, not NoneType"
        if is_cpython
        else "'NoneType' does not have the buffer interface"
    )

    assert that(assertions).raises(TypeError, error_msg)


def test_that_none_contains_string():
    "that(None).contains('bungalow')"

    try:
        assert that(None).contains("bungalow")
        assert False, "should not reach here"
    except Exception as e:
        error_msg = (
            "argument of type 'NoneType' is not iterable"
            if is_cpython
            else "'NoneType' object is not iterable"
        )
        expects(str(e)).when.called_with(error_msg)


def test_that_some_iterable_is_empty():
    "that(some_iterable).is_empty and that(data_structure).are_empty"

    assert that([]).is_empty
    assert that([]).are_empty

    assert that(tuple()).is_empty
    assert that({}).are_empty

    def fail_single():
        assert that((1,)).is_empty

    assert that(fail_single).raises("(1,) is not empty, it has 1 item")

    def fail_plural():
        assert that((1, 2)).is_empty

    assert that(fail_plural).raises("(1, 2) is not empty, it has 2 items")


def test_that_data_structure_is_empty_raises():
    "that(data_structure_not_iterable).is_empty and that(data_structure_not_iterable).are_empty raises"

    obj = object()

    def fail():
        assert that(obj).is_empty
        assert False, "should not reach here"

    assert that(fail).raises("%r is not iterable" % obj)


def test_that_data_structure_iterable_matches_another():
    "that(data_structure_iterable).matches(another_iterable)"

    KlassOne = type("KlassOne", (object,), {})
    KlassTwo = type("KlassTwo", (object,), {})
    one = [
        ("/1", KlassOne),
        ("/2", KlassTwo),
    ]

    two = [
        ("/1", KlassOne),
        ("/2", KlassTwo),
    ]

    assert that(one).matches(two)
    assert that(one).equals(two)

    def fail_1():
        assert that([1]).matches(range(2))

    class Fail2(object):
        def __init__(self):
            assert that(range(1)).matches([2])

    class Fail3(object):
        def __call__(self):
            assert that(range(1)).matches([2])

    range_name = range.__name__
    assert that(fail_1).raises("X is a list and Y is a {0} instead".format(range_name))
    assert that(Fail2).raises("X is a {0} and Y is a list instead".format(range_name))
    assert that(Fail3()).raises(
        "X is a {0} and Y is a list instead".format(range_name)
    )


def test_within_pass():
    "within(four=miliseconds) will pass"

    within(four=miliseconds)(lambda *a: None)()


def test_within_five_milicesonds_fails_when_function_takes_six_miliseconds():
    "within(five=miliseconds) should fail when the decorated function takes six miliseconds to run"

    def sleepy(*a):
        time.sleep(0.6)

    failed = False
    try:
        within(five=miliseconds)(sleepy)()
    except AssertionError as e:
        failed = True
        expects("sleepy [tests/test_original_api.py line 667] did not run within five miliseconds").to.equal(str(e))

    assert failed, "within(five=miliseconds)(sleepy) did not fail"


def test_word_to_number():
    expects(sure.word_to_number("one")).to.equal(1)
    expects(sure.word_to_number("two")).to.equal(2)
    expects(sure.word_to_number("three")).to.equal(3)
    expects(sure.word_to_number("four")).to.equal(4)
    expects(sure.word_to_number("five")).to.equal(5)
    expects(sure.word_to_number("six")).to.equal(6)
    expects(sure.word_to_number("seven")).to.equal(7)
    expects(sure.word_to_number("eight")).to.equal(8)
    expects(sure.word_to_number("nine")).to.equal(9)
    expects(sure.word_to_number("ten")).to.equal(10)
    expects(sure.word_to_number("eleven")).to.equal(11)
    expects(sure.word_to_number("twelve")).to.equal(12)
    expects(sure.word_to_number("thirteen")).to.equal(13)
    expects(sure.word_to_number("fourteen")).to.equal(14)
    expects(sure.word_to_number("fifteen")).to.equal(15)
    expects(sure.word_to_number("sixteen")).to.equal(16)


def test_word_to_number_fail():
    failed = False
    try:
        sure.word_to_number("twenty")
    except AssertionError as e:
        failed = True
        expects(str(e)).to.equal(
            "sure supports only literal numbers from one "
            'to sixteen, you tried the word "twenty"'
        )

    assert failed, "should raise assertion error"


def test_microsecond_unit():
    "testing microseconds convertion"
    cfrom, cto = sure.UNITS[sure.microsecond]

    expects(cfrom(1)).to.equal(100000)
    expects(cto(1)).to.equal(1)

    cfrom, cto = sure.UNITS[sure.microseconds]

    expects(cfrom(1)).to.equal(100000)
    expects(cto(1)).to.equal(1)


def test_milisecond_unit():
    "testing miliseconds convertion"
    cfrom, cto = sure.UNITS[sure.milisecond]

    expects(cfrom(1)).to.equal(1000)
    expects(cto(100)).to.equal(1)

    cfrom, cto = sure.UNITS[sure.miliseconds]

    expects(cfrom(1)).to.equal(1000)
    expects(cto(100)).to.equal(1)


def test_second_unit():
    "testing seconds convertion"
    cfrom, cto = sure.UNITS[sure.second]

    expects(cfrom(1)).to.equal(1)
    expects(cto(100000)).to.equal(1)

    cfrom, cto = sure.UNITS[sure.seconds]

    expects(cfrom(1)).to.equal(1)
    expects(cto(100000)).to.equal(1)


def test_minute_unit():
    "testing minutes convertion"
    cfrom, cto = sure.UNITS[sure.minute]

    expects(cfrom(60)).to.equal(1)
    expects(cto(1)).to.equal(6000000)

    cfrom, cto = sure.UNITS[sure.minutes]

    expects(cfrom(60)).to.equal(1)
    expects(cto(1)).to.equal(6000000)


def test_within_wrong_usage():
    "within(three=miliseconds, one=second) should raise WrongUsageError"

    expects(within).when.called_with(three=miliseconds, one=second).to.have.raised(
        WrongUsageError,
        "within() takes a single keyword argument where the argument must be a numerical description from one to eighteen and the value. For example: within(eighteen=miliseconds)"
    )


def test_that_is_a_matcher_should_absorb_callables_to_be_used_as_matcher():
    "that.is_a_matcher should absorb callables to be used as matcher"

    @that.is_a_matcher
    def is_truthful(what):
        assert bool(what), "%s is so untrue" % (what)
        return "foobar"

    assert that("friend").is_truthful()
    expects(that("friend").is_truthful()).to.equal("foobar")


def test_accepts_setup_list():
    "sure.with_context() accepts a list of callbacks for setup"

    def setup1(context):
        context.first_action = "seek"

    def setup2(context):
        context.last_action = "truth"

    @sure.that_with_context([setup1, setup2])
    def actions_are_within_context(context):
        assert context.first_action == "seek"
        assert context.last_action == "truth"

    actions_are_within_context()

    # expects the name of the decorated function to not undergo a name change
    expects(actions_are_within_context.__name__).to.equal(
        "actions_are_within_context",
    )


def test_accepts_teardown_list():
    "sure.with_context() runs teardown before the function itself"

    class data_structure:
        modified = True
        finished = "nope"

    def setup(context):
        data_structure.modified = False

    def teardown1(context):
        data_structure.modified = True

    def teardown2(context):
        data_structure.finished = "yep"

    @sure.that_with_context(setup, [teardown1, teardown2])
    def data_structure_was_modified(context):
        assert not data_structure.modified
        assert data_structure.finished == "nope"

    data_structure_was_modified()
    assert data_structure.modified
    assert data_structure.finished == "yep"


def test_scenario_is_alias_for_context_on_setup_and_teardown():
    "@scenario aliases @that_with_context for setup and teardown"

    def setup(context):
        context.name = "Robert C. Martin"

    def teardown(context):
        expects(context.name).to.equal("Robert C. Martin")

    @scenario([setup], [teardown])
    def robert_is_within_context(context):
        "Robert is within context"
        assert isinstance(context, StagingArea)
        assert hasattr(context, "name")
        expects(context.name).to.equal("Robert C. Martin")

    robert_is_within_context()
    expects(robert_is_within_context.__name__).to.equal(
        "robert_is_within_context",
    )


def test_actions_returns_context():
    "the actions always returns the context"

    def with_setup(context):
        @action_for(context)
        def action1():
            pass

        @action_for(context)
        def action2():
            pass

    @scenario(with_setup)
    def i_can_use_actions(context):
        assert that(context.action1()).equals(context)
        assert that(context.action2()).equals(context)
        return True

    assert i_can_use_actions()


def test_actions_providing_variables_in_the_context():
    "the actions should be able to declare the variables they provide"

    def with_setup(context):
        @action_for(context, provides=["var1", "foobar"])
        def the_context_has_variables():
            context.var1 = 123
            context.foobar = "qwerty"

    @scenario(with_setup)
    def the_providers_are_working(Then):
        Then.the_context_has_variables()
        assert hasattr(Then, "var1")
        assert hasattr(Then, "foobar")
        assert hasattr(Then, "__sure_providers_of__")

        providers = Then.__sure_providers_of__
        action = Then.the_context_has_variables.__name__

        providers_of_var1 = [p.__name__ for p in providers["var1"]]
        assert that(providers_of_var1).contains(action)

        providers_of_foobar = [p.__name__ for p in providers["foobar"]]
        assert that(providers_of_foobar).contains(action)

        return True

    assert the_providers_are_working()


def test_fails_when_action_doesnt_fulfill_the_agreement_of_its_provides_argument():
    "it fails when an action doesn't fulfill its agreements"

    error = (
        'the action "unreasonable_action" is supposed to provide the '
        'attribute "two" into the context but does not. '
        'Check its implementation for correctness or, if '
        'there is a bug in Sure, consider reporting that at '
        'https://github.com/gabrielfalcao/sure/issues'
    )

    def with_setup(context):
        @action_for(context, provides=["one", "two"])
        def unreasonable_action():
            context.one = 123

    @scenario(with_setup)
    def reasoning_of_an_unreasonable_action(context):
        expects(context.unreasonable_action).to.have.raised(AssertionError, error)
        return 'relativist'

    expects(reasoning_of_an_unreasonable_action).when.called.to.return_value('relativist')


def test_depends_on_failing_due_to_lack_of_attribute_in_context():
    "it fails when an action depends on some attribute that is not " "provided by any other previous action"

    fullpath = collapse_path(os.path.abspath(__file__))
    error = (
        f'the action "variant_action" defined at {fullpath}:942 '
        'depends on the attribute "data_structure" to be available in the'
        " current context"
    )

    def with_setup(context):
        @action_for(context, depends_on=["data_structure"])
        def variant_action():
            pass

    @scenario(with_setup)
    def depends_on_fails(the):
        assert that(the.variant_action).raises(AssertionError, error)
        return True

    assert depends_on_fails()


def test_depends_on_failing_due_not_calling_a_previous_action():
    "it fails when an action depends on some attribute that is being " "provided by other actions"

    fullpath = collapse_path(os.path.abspath(__file__))
    error = (
        'the action "my_action" defined at {0}:970 '
        'depends on the attribute "some_attr" to be available in the context.'
        " Perhaps one of the following actions might provide that attribute:\n"
        " -> dependency_action at {0}:966".replace("{0}", fullpath)
    )

    def with_setup(context):
        @action_for(context, provides=["some_attr"])
        def dependency_action():
            context.some_attr = True

        @action_for(context, depends_on=["some_attr"])
        def my_action():
            pass

    @scenario(with_setup)
    def depends_on_fails(the):
        assert that(the.my_action).raises(AssertionError, error)
        return True

    assert depends_on_fails()


def test_that_contains_dictionary_keys():
    "that(dict(name='foobar')).contains('name')"

    data = dict(name="foobar")
    assert "name" in data
    assert "name" in data.keys()
    assert that(data).contains("name")


def test_that_contains_list():
    "that(['foobar', '123']).contains('foobar')"

    data = ["foobar", "123"]
    assert "foobar" in data
    assert that(data).contains("foobar")


def test_that_contains_set():
    "that(set(['foobar', '123']).contains('foobar')"

    data = set(["foobar", "123"])
    assert "foobar" in data
    assert that(data).contains("foobar")


def test_that_contains_tuple():
    "that(('foobar', '123')).contains('foobar')"

    data = ("foobar", "123")
    assert "foobar" in data
    assert that(data).contains("foobar")


def test_staging_area_provides_meaningful_error_on_nonexisting_attribute():
    "StagingArea() provides a meaningful error when attr does not exist"

    context = StagingArea()

    context.bar = "bar"
    context.foo = "foo"

    assert that(context.bar).equals("bar")
    assert that(context.foo).equals("foo")

    def access_nonexisting_attribute():
        assert context.nonexisting == "attribute"

    assert that(access_nonexisting_attribute).raises(
        AssertionError,
        "attempt to access attribute with name `nonexisting' from the context "
        "(also known as `StagingArea'), but there is no such attribute assigned to it. "
        "The presently available attributes in this context are: "
        "['bar', 'foo']",
    )


def test_actions_providing_dinamically_named_variables():
    "the actions should be able to declare the variables they provide"

    def with_setup(context):
        @action_for(context, provides=["var1", "{0}"])
        def the_context_has_variables(first_arg):
            context.var1 = 123
            context[first_arg] = "qwerty"

    @scenario(with_setup)
    def the_providers_are_working(Then):
        Then.the_context_has_variables("worker")
        assert hasattr(Then, "var1")
        assert "worker" in Then
        assert hasattr(Then, "__sure_providers_of__")

        providers = Then.__sure_providers_of__
        action = Then.the_context_has_variables.__name__

        providers_of_var1 = [p.__name__ for p in providers["var1"]]
        assert that(providers_of_var1).contains(action)

        providers_of_worker = [p.__name__ for p in providers["worker"]]
        assert that(providers_of_worker).contains(action)

        return True

    assert the_providers_are_working()


def test_deep_equals_dict_level1_success():
    "that() deep_equals(dict) succeeding on level 1"

    data_structure = {
        "one": "yeah",
    }

    assert that(data_structure).deep_equals(
        {
            "one": "yeah",
        }
    )


def test_deep_equals_dict_level1_fail():
    "that() deep_equals(dict) failing on level 1"

    data_structure = {
        "one": "yeah",
    }

    def assertions():
        assert that(data_structure).deep_equals(
            {
                "one": "oops",
            }
        )

    assert that(assertions).raises(
        AssertionError,
        "X = {'one': 'yeah'}\n"
        "    and\n"
        "Y = {'one': 'oops'}\n"
        "X['one'] is 'yeah' whereas Y['one'] is 'oops'",
    )


def test_deep_equals_list_level1_success():
    "that(list) deep_equals(list) succeeding on level 1"

    data_structure = ["one", "yeah"]
    assert that(data_structure).deep_equals(["one", "yeah"])


def test_deep_equals_list_level1_fail_by_value():
    "that(list) deep_equals(list) failing on level 1"

    data_structure = ["one", "yeahs"]

    def assertions():
        assert that(data_structure).deep_equals(["one", "yeah"])

    assert that(assertions).raises(
        AssertionError,
        "X = ['one', 'yeahs']\n"
        "    and\n"
        "Y = ['one', 'yeah']\n"
        "X[1] is 'yeahs' whereas Y[1] is 'yeah'",
    )


def test_deep_equals_list_level1_fail_by_length_x_gt_y():
    "that(list) deep_equals(list) failing by length (len(X) > len(Y))"

    data_structure = ["one", "yeah", "awesome!"]

    def assertions():
        assert that(data_structure).deep_equals(["one", "yeah"])

    assert that(assertions).raises(
        AssertionError,
        "X = ['one', 'yeah', 'awesome!']\n"
        "    and\n"
        "Y = ['one', 'yeah']\n"
        "X has 3 items whereas Y has only 2",
    )


def test_deep_equals_list_level1_fail_by_length_y_gt_x():
    "that(list) deep_equals(list) failing by length (len(Y) > len(X))"

    data_structure = ["one", "yeah"]

    def assertions():
        assert that(data_structure).deep_equals(["one", "yeah", "damn"])

    assert that(assertions).raises(
        AssertionError,
        "X = ['one', 'yeah']\n"
        "    and\n"
        "Y = ['one', 'yeah', 'damn']\n"
        "Y has 3 items whereas X has only 2"
    )


def test_deep_equals_dict_level1_fails_missing_key_on_y():
    "that(X) deep_equals(Y) fails when Y is missing a key that X has"

    data_structure = {
        "three": "value",
    }

    def assertions():
        assert that(data_structure).deep_equals(
            {
                "two": "value",
            }
        )

    assert that(assertions).raises(
        AssertionError,
        "X = {'three': 'value'}\n"
        "    and\n"
        "Y = {'two': 'value'}\n"
        "X has the key \"'three'\" whereas Y does not"
    )


def test_deep_equals_failing_basic_vs_complex():
    "that(X) deep_equals(Y) fails with basic vc complex type"

    def assertions():
        assert that("two yeah").deep_equals(
            {
                "two": "yeah",
            }
        )

    assert that(assertions).raises(
        AssertionError,
        "X = 'two yeah'\n"
        "    and\n"
        "Y = {'two': 'yeah'}\n"
        "X is a %s and Y is a dict instead" % str.__name__,
    )


def test_deep_equals_failing_complex_vs_basic():
    "that(X) deep_equals(Y) fails with complex vc basic type"

    def assertions():
        assert that({"two": "yeah"}).deep_equals("two yeah")

    assert that(assertions).raises(
        AssertionError,
        "X = {'two': 'yeah'}\n"
        "    and\n"
        "Y = 'two yeah'\n"
        "X is a dict and Y is a %s instead" % str.__name__,
    )


def test_deep_equals_tuple_level1_success():
    "that(tuple) deep_equals(tuple) succeeding on level 1"

    data_structure = ("one", "yeah")
    assert that(data_structure).deep_equals(("one", "yeah"))


def test_deep_equals_tuple_level1_fail_by_value():
    "that(tuple) deep_equals(tuple) failing on level 1"

    data_structure = ("one", "yeahs")

    def assertions():
        assert that(data_structure).deep_equals(("one", "yeah"))

    assert that(assertions).raises(
        AssertionError,
        "X = ('one', 'yeahs')\n"
        "    and\n"
        "Y = ('one', 'yeah')\n"
        "X[1] is 'yeahs' whereas Y[1] is 'yeah'",
    )


def test_deep_equals_tuple_level1_fail_by_length_x_gt_y():
    "that(tuple) deep_equals(tuple) failing by length (len(X) > len(Y))"

    data_structure = ("one", "yeah", "awesome!")

    def assertions():
        assert that(data_structure).deep_equals(("one", "yeah"))

    assert that(assertions).raises(
        AssertionError,
        "X = ('one', 'yeah', 'awesome!')\n"
        "    and\n"
        "Y = ('one', 'yeah')\n"
        "X has 3 items whereas Y has only 2",
    )


def test_deep_equals_tuple_level1_fail_by_length_y_gt_x():
    "that(tuple) deep_equals(tuple) failing by length (len(Y) > len(X))"

    data_structure = ("one", "yeah")

    def assertions():
        assert that(data_structure).deep_equals(("one", "yeah", "damn"))

    assert that(assertions).raises(
        AssertionError,
        "X = ('one', 'yeah')\n"
        "    and\n"
        "Y = ('one', 'yeah', 'damn')\n"
        "Y has 3 items whereas X has only 2",
    )


def test_deep_equals_fallsback_to_generic_comparator():
    "that() deep_equals(dict) falling back to generic comparator"
    from datetime import datetime

    now = datetime.now()
    data_structure = {
        "one": "yeah",
        "date": now,
    }

    assert that(data_structure).deep_equals(
        {
            "one": "yeah",
            "date": now,
        }
    )


def test_deep_equals_fallsback_to_generic_comparator_failing():
    "that() deep_equals(dict) with generic comparator failing"
    from datetime import datetime

    now = datetime(2012, 3, 5)
    tomorrow = datetime(2012, 3, 6)
    data_structure = {
        "date": now,
    }

    def assertions():
        assert that(data_structure).deep_equals(
            {
                "date": tomorrow,
            }
        )

    assert that(assertions).raises(
        AssertionError,
        "X = {'date': datetime.datetime(2012, 3, 5, 0, 0)}\n"
        "    and\n"
        "Y = {'date': datetime.datetime(2012, 3, 6, 0, 0)}\n"
        "X['date'] != Y['date']",
    )


def test_deep_equals_fallsback_to_generic_comparator_failing_type():
    "that() deep_equals(dict) with generic comparator failing"
    from datetime import datetime

    now = datetime(2012, 3, 5)
    data_structure = {
        "date": now,
    }

    def assertions():
        assert that(data_structure).deep_equals(
            {
                "date": None,
            }
        )

    assert that(assertions).raises(
        AssertionError,
        "X = {'date': datetime.datetime(2012, 3, 5, 0, 0)}\n"
        "    and\n"
        "Y = {'date': None}\n"
        "X['date'] is a datetime and Y['date'] is a NoneType instead",
    )


def test_deep_equals_dict_level2_success():
    "that() deep_equals(dict) succeeding on level 2"

    data_structure = {
        "one": "yeah",
        "another": {
            "two": "cool",
        },
    }

    assert that(data_structure).deep_equals(
        {
            "one": "yeah",
            "another": {
                "two": "cool",
            },
        }
    )


def test_deep_equals_dict_level2_list_success():
    "that() deep_equals(dict) succeeding on level 2"

    data_structure = {
        "one": "yeah",
        "another": ["one", "two", 3],
    }

    assert that(data_structure).deep_equals(
        {
            "one": "yeah",
            "another": ["one", "two", 3],
        }
    )


def test_deep_equals_dict_level2_fail():
    "that() deep_equals(dict) failing on level 2"

    data_structure = {
        "word": "reasonable",
        "another": {
            "word": "unreason",
        },
    }

    def assertions():
        assert that(data_structure).deep_equals(
            {
                "word": "reasonable",
                "another": {
                    "word": "reason",
                },
            }
        )

    assert that(assertions).raises(
        AssertionError,
        "X = {'word': 'reasonable', 'another': {'word': 'unreason'}}\n"
        "    and\n"
        "Y = {'word': 'reasonable', 'another': {'word': 'reason'}}\n"
        "X['another']['word'] is 'unreason' whereas Y['another']['word'] is 'reason'",
    )


def test_deep_equals_dict_level3_fail_values():
    "that() deep_equals(dict) failing on level 3"

    data_structure = {
        "index": [
            {"name": "JC", "age": 33},
        ],
    }

    def assertions():
        assert that(data_structure).deep_equals(
            {
                "index": [
                    {"name": "JC", "age": 31},
                ],
            }
        )

    assert that(assertions).raises(
        AssertionError,
        "X = {'index': [{'name': 'JC', 'age': 33}]}\n"
        "    and\n"
        "Y = {'index': [{'name': 'JC', 'age': 31}]}\n"
        "X['index'][0]['age'] is 33 whereas Y['index'][0]['age'] is 31",
    )


def test_deep_equals_dict_level3_fails_missing_key():
    "that() deep_equals(dict) failing on level 3 when missing a key"

    data_structure = {
        "index": [
            {"age": 33, "name": "JC"},
        ],
    }

    def assertions():
        assert that(data_structure).deep_equals(
            {
                "index": [
                    {"age": 31, "foo": "bar", "name": "JC"},
                ],
            }
        )

    assert that(assertions).raises(
        AssertionError,
        "X = {'index': [{'age': 33, 'name': 'JC'}]}\n"
        "    and\n"
        "Y = {'index': [{'age': 31, 'foo': 'bar', 'name': 'JC'}]}\n"
        "X['index'][0] does not have the key \"'foo'\" whereas Y['index'][0] has it"
    )


def test_deep_equals_dict_level3_fails_extra_key():
    "that() deep_equals(dict) failing on level 3 when has an extra key"

    data_structure = {
        "index": [
            {"age": 33, "foo": "bar", "name": "JC"},
        ],
    }

    def assertions():
        assert that(data_structure).deep_equals(
            {
                "index": [
                    {"age": 31, "name": "JC"},
                ],
            }
        )

    assert that(assertions).raises(
        AssertionError,
        "X = {'index': [{'age': 33, 'foo': 'bar', 'name': 'JC'}]}\n"
        "    and\n"
        "Y = {'index': [{'age': 31, 'name': 'JC'}]}\n"
        "X['index'][0] has the key \"'foo'\" whereas Y['index'][0] does not"
    )


def test_deep_equals_dict_level3_fails_different_key():
    "that() deep_equals(dict) failing on level 3 when has an extra key"

    data_structure = {
        "index": [
            {"age": 33, "foo": "bar", "name": "JC"},
        ],
    }

    def assertions():
        assert that(data_structure).deep_equals(
            {
                "index": [
                    {"age": 33, "bar": "foo", "name": "JC"},
                ],
            }
        )

    assert that(assertions).raises(
        AssertionError,
        "X = {'index': [{'age': 33, 'foo': 'bar', 'name': 'JC'}]}\n"
        "    and\n"
        "Y = {'index': [{'age': 33, 'bar': 'foo', 'name': 'JC'}]}\n"
        "X['index'][0] has the key \"'foo'\" whereas Y['index'][0] does not"
    )


def test_deep_equals_list_level2_fail_by_length_x_gt_y():
    "that(list) deep_equals(list) failing by length (len(X) > len(Y))"

    data_structure = {"iterable": ["one", "yeah", "awesome!"]}

    def assertions():
        assert that(data_structure).deep_equals({"iterable": ["one", "yeah"]})

    assert that(assertions).raises(
        AssertionError,
        "X = {'iterable': ['one', 'yeah', 'awesome!']}\n"
        "    and\n"
        "Y = {'iterable': ['one', 'yeah']}\n"
        "X['iterable'] has 3 items whereas Y['iterable'] has only 2",
    )


def test_deep_equals_list_level2_fail_by_length_y_gt_x():
    "that(list) deep_equals(list) failing by length (len(Y) > len(X))"

    data_structure = ["one", "yeah"]

    def assertions():
        assert that(data_structure).deep_equals(["one", "yeah", "damn"])

    assert that(assertions).raises(
        AssertionError,
        "X = ['one', 'yeah']\n"
        "    and\n"
        "Y = ['one', 'yeah', 'damn']\n"
        "Y has 3 items whereas X has only 2",
    )


def test_function_decorated_with_wip_should_set_a_flag():
    "@sure.work_in_progress should set an internal flag into `sure`"

    @sure.work_in_progress
    def this_was_called():
        assert sure.it("is_running")
        return True

    assert not sure._registry["is_running"]
    assert this_was_called()
    assert not sure._registry["is_running"]


def test_that_equals_fails():
    "that() equals(string) when it's supposed to fail"

    something = "else"

    def fail():
        assert that("something").equals(something)

    assert that(fail).raises(
        AssertionError,
        "X = 'something'\n"
        "    and\n"
        "Y = 'else'\n"
        "X is 'something' whereas Y is 'else'",
    )


def test_raises_with_string():
    "that(callable).raises('message') should compare the message"
    def it_fails():
        raise AssertionError("should fail with this exception")

    try:
        expects(it_fails).raises("wrong msg")
        raise AssertionError("should not reach here")
    except AssertionError as e:
        error = e
        expects(str(error)).to.contain(
            """ACTUAL:
should fail with this exception

EXPECTATION:
wrong msg"""
        )


def test_deep_comparison_sequences_of_sequences():
    part1 = [
        ("Bootstraping Redis role", []),
        ("Restart scalarizr", []),
        ("Rebundle server", ["rebundle"]),
        ("Use new role", ["rebundle"]),
        ("Restart scalarizr after bundling", ["rebundle"]),
        ("Bundling data", []),
        ("Modifying data", []),
        ("Reboot server", []),
        ("Backuping data on Master", []),
        ("Setup replication", []),
        ("Restart scalarizr in slave", []),
        ("Slave force termination", []),
        ("Slave delete EBS", ["ec2"]),
        ("Setup replication for EBS test", ["ec2"]),
        ("Writing on Master, reading on Slave", []),
        ("Slave -> Master promotion", []),
        ("Restart farm", ["restart_farm"]),
    ]

    part2 = [
        ("Bootstraping Redis role", ["rebundle", "rebundle", "rebundle"]),
        ("Restart scalarizr", []),
        ("Rebundle server", ["rebundle"]),
        ("Use new role", ["rebundle"]),
        ("Restart scalarizr after bundling", ["rebundle"]),
        ("Bundling data", []),
        ("Modifying data", []),
        ("Reboot server", []),
        ("Backuping data on Master", []),
        ("Setup replication", []),
        ("Restart scalarizr in slave", []),
        ("Slave force termination", []),
        ("Slave delete EBS", ["ec2"]),
        ("Setup replication for EBS test", ["ec2"]),
        ("Writing on Master, reading on Slave", []),
        ("Slave -> Master promotion", []),
        ("Restart farm", ["restart_farm"]),
    ]

    try:
        expects(part1).equals(part2)
    except AssertionError as e:
        expects(str(e)).to_not.be.different_of("""Equality Error
X = [('Bootstraping Redis role', []), ('Restart scalarizr', []), ('Rebundle server', ['rebundle']), ('Use new role', ['rebundle']), ('Restart scalarizr after bundling', ['rebundle']), ('Bundling data', []), ('Modifying data', []), ('Reboot server', []), ('Backuping data on Master', []), ('Setup replication', []), ('Restart scalarizr in slave', []), ('Slave force termination', []), ('Slave delete EBS', ['ec2']), ('Setup replication for EBS test', ['ec2']), ('Writing on Master, reading on Slave', []), ('Slave -> Master promotion', []), ('Restart farm', ['restart_farm'])]
    and
Y = [('Bootstraping Redis role', ['rebundle', 'rebundle', 'rebundle']), ('Restart scalarizr', []), ('Rebundle server', ['rebundle']), ('Use new role', ['rebundle']), ('Restart scalarizr after bundling', ['rebundle']), ('Bundling data', []), ('Modifying data', []), ('Reboot server', []), ('Backuping data on Master', []), ('Setup replication', []), ('Restart scalarizr in slave', []), ('Slave force termination', []), ('Slave delete EBS', ['ec2']), ('Setup replication for EBS test', ['ec2']), ('Writing on Master, reading on Slave', []), ('Slave -> Master promotion', []), ('Restart farm', ['restart_farm'])]
Y[0][1] has 3 items whereas X[0][1] is empty
""".strip())


def test_within_failing_due_to_internally_raised_exception():
    "within(ten=miliseconds) should fail when the decorated function raises an unrelated exception"

    def crash(*a):
        time.sleep(0.1)
        raise RuntimeError('unrelated exception')

    expects(within(five=miliseconds)(crash)).when.called.to.have.raised(
        RuntimeError,
        "unrelated exception"
    )


def test_all_integers_at_least_one_element_not_an_integer():
    ":func:`sure.original.all_integers` returns False when at least one of the elements in the given iterable is not a :class:`int`"

    expects(all_integers([1, 2, 3, "four"])).to.be.false


def test_all_integers_not_iterable():
    ":func:`sure.original.all_integers` returns False when receiving a non-iterable param"

    expects(all_integers(9)).to.be.false
