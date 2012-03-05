# #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - assertion toolbox>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import sure
from sure import that, VariablesBag
from nose.tools import assert_equals, assert_raises


def test_setup_with_context():
    "sure.with_context() runs setup before the function itself"

    def setup(context):
        context.name = "John Resig"

    @sure.that_with_context(setup)
    def john_is_within_context(context):
        assert isinstance(context, VariablesBag)
        assert hasattr(context, "name")

    john_is_within_context()
    assert_equals(
        john_is_within_context.__name__,
        'john_is_within_context',
    )


def test_context_is_not_optional():
    "sure.that_with_context() when no context is given it fails"

    def setup(context):
        context.name = "John Resig"

    @sure.that_with_context(setup)
    def it_crashes():
        assert True

    assert that(it_crashes).raises(
        TypeError,
        "the function it_crashes defined at test_sure.py line 57, is being " \
        "decorated by either @that_with_context or @scenario, so it should " \
        "take at least 1 parameter, which is the test context",
    )


def test_setup_with_context_context_failing():
    "sure.that_with_context() in a failing test"

    def setup(context):
        context.name = "John Resig"

    @sure.that_with_context(setup)
    def it_fails(context):
        assert False, 'should fail with this exception'

    assert that(it_fails).raises('should fail with this exception')


def test_teardown_with_context():
    "sure.with_context() runs teardown before the function itself"

    class something:
        pass

    def setup(context):
        something.modified = True

    def teardown(context):
        del something.modified

    @sure.that_with_context(setup, teardown)
    def something_was_modified(context):
        assert hasattr(something, "modified")
        assert something.modified

    something_was_modified()
    assert not hasattr(something, "modified")


def test_that_is_a():
    "sure.that() is_a(object)"

    something = "something"

    assert that(something).is_a(str)
    assert isinstance(something, str)


def test_that_equals():
    "sure.that() equals(string)"

    something = "something"

    assert that('something').equals(something)
    assert something == 'something'


def test_that_differs():
    "sure.that() differs(object)"

    something = "something"

    assert that(something).differs("23123%FYTUGIHOfdf")
    assert something != "23123%FYTUGIHOfdf"


def test_that_has():
    "sure.that() has(object)"

    class Class:
        name = "some class"
    Object = Class()
    dictionary = {
        'name': 'John',
    }
    name = "john"

    assert hasattr(Class, 'name')
    assert that(Class).has("name")
    assert that(Class).like("name")
    assert "name" in sure.that(Class)

    assert hasattr(Object, 'name')
    assert that(Object).has("name")
    assert that(Object).like("name")
    assert "name" in sure.that(Object)

    assert dictionary.has_key('name')
    assert that(dictionary).has("name")
    assert that(dictionary).like("name")
    assert "name" in sure.that(dictionary)

    assert that(name).has("john")
    assert that(name).like("john")
    assert "john" in sure.that(name)
    assert that(name).has("hn")
    assert that(name).like("hn")
    assert "hn" in sure.that(name)
    assert that(name).has("jo")
    assert that(name).like("jo")
    assert "jo" in sure.that(name)


def test_that_at_key_equals():
    "sure.that().at(object).equals(object)"

    class Class:
        name = "some class"
    Object = Class()
    dictionary = {
        'name': 'John',
    }

    assert that(Class).at("name").equals('some class')
    assert that(Object).at("name").equals('some class')
    assert that(dictionary).at("name").equals('John')


def test_that_len_is():
    "sure.that() len_is(number)"

    lst = range(1000)

    assert that(lst).len_is(1000)
    assert len(lst) == 1000
    assert that(lst).len_is(lst)


def test_that_len_greater_than():
    "sure.that() len_greater_than(number)"

    lst = range(1000)
    lst2 = range(100)

    assert that(lst).len_greater_than(100)
    assert len(lst) == 1000
    assert that(lst).len_greater_than(lst2)


def test_that_len_greater_than_should_raise_assertion_error():
    "sure.that() len_greater_than(number) raise AssertionError"

    lst = range(1000)
    try:
        that(lst).len_greater_than(1000)
    except AssertionError, e:
        assert_equals(
            str(e),
            'the length of the list should be greater then %d, but is %d'  \
            % (1000, 1000))


def test_that_len_greater_than_or_equals():
    "sure.that() len_greater_than_or_equals(number)"

    lst = range(1000)
    lst2 = range(100)

    assert that(lst).len_greater_than_or_equals(100)
    assert that(lst).len_greater_than_or_equals(1000)
    assert len(lst) == 1000
    assert that(lst).len_greater_than_or_equals(lst2)
    assert that(lst).len_greater_than_or_equals(lst)


def test_that_len_greater_than_or_equals_should_raise_assertion_error():
    "sure.that() len_greater_than_or_equals(number) raise AssertionError"

    lst = range(1000)
    try:
        that(lst).len_greater_than_or_equals(1001)
    except AssertionError, e:
        assert_equals(
            str(e),
            'the length of %r should be greater then or equals %d, but is %d' \
            % (lst, 1001, 1000))


def test_that_len_lower_than():
    "sure.that() len_lower_than(number)"

    lst = range(100)
    lst2 = range(1000)

    assert that(lst).len_lower_than(101)
    assert len(lst) == 100
    assert that(lst).len_lower_than(lst2)


def test_that_len_lower_than_should_raise_assertion_error():
    "sure.that() len_lower_than(number) raise AssertionError"

    lst = range(1000)
    try:
        that(lst).len_lower_than(1000)
    except AssertionError, e:
        assert_equals(
            str(e),
            'the length of %r should be lower then %d, but is %d' % \
            (lst, 1000, 1000))


def test_that_len_lower_than_or_equals():
    "sure.that() len_lower_than_or_equals(number)"

    lst = range(1000)
    lst2 = range(1001)

    assert that(lst).len_lower_than_or_equals(1001)
    assert that(lst).len_lower_than_or_equals(1000)
    assert len(lst) == 1000
    assert that(lst).len_lower_than_or_equals(lst2)
    assert that(lst).len_lower_than_or_equals(lst)


def test_that_len_lower_than_or_equals_should_raise_assertion_error():
    "sure.that() len_lower_than_or_equals(number) raise AssertionError"

    lst = range(1000)
    try:
        that(lst).len_lower_than_or_equals(100)
    except AssertionError, e:
        assert_equals(
            str(e),
            'the length of %r should be lower then or equals %d, but is %d' % \
            (lst, 100, 1000))


def test_that_checking_all_atributes():
    "sure.that(iterable).the_attribute('name').equals('value')"
    class shape(object):
        def __init__(self, name):
            self.kind = 'geometrical form'
            self.name = name

    shapes = [
        shape('circle'),
        shape('square'),
        shape('rectangle'),
        shape('triangle'),
    ]

    assert that(shapes).the_attribute("kind").equals('geometrical form')


def test_that_checking_all_atributes_of_range():
    "sure.that(iterable, within_range=(1, 2)).the_attribute('name').equals('value')"
    class shape(object):
        def __init__(self, name):
            self.kind = 'geometrical form'
            self.name = name

        def __repr__(self):
            return '<%s:%s>' % (self.kind, self.name)

    shapes = [
        shape('circle'),
        shape('square'),
        shape('square'),
        shape('triangle'),
    ]

    assert shapes[0].name != 'square'
    assert shapes[3].name != 'square'

    assert shapes[1].name == 'square'
    assert shapes[2].name == 'square'

    assert that(shapes, within_range=(1, 2)). \
                           the_attribute("name"). \
                           equals('square')


def test_that_checking_all_elements():
    "sure.that(iterable).every_one_is('value')"
    shapes = [
        'cube',
        'ball',
        'ball',
        'piramid',
    ]

    assert shapes[0] != 'ball'
    assert shapes[3] != 'ball'

    assert shapes[1] == 'ball'
    assert shapes[2] == 'ball'

    assert that(shapes, within_range=(1, 2)).every_one_is('ball')


def test_that_checking_each_matches():
    "sure.that(iterable).in_each('').equals('value')"
    class animal(object):
        def __init__(self, kind):
            self.attributes = {
                'class': 'mammal',
                'kind': kind,
            }

    animals = [
        animal('dog'),
        animal('cat'),
        animal('cow'),
        animal('cow'),
        animal('cow'),
    ]

    assert animals[0].attributes['kind'] != 'cow'
    assert animals[1].attributes['kind'] != 'cow'

    assert animals[2].attributes['kind'] == 'cow'
    assert animals[3].attributes['kind'] == 'cow'
    assert animals[4].attributes['kind'] == 'cow'

    assert animals[0].attributes['class'] == 'mammal'
    assert animals[1].attributes['class'] == 'mammal'
    assert animals[2].attributes['class'] == 'mammal'
    assert animals[3].attributes['class'] == 'mammal'
    assert animals[4].attributes['class'] == 'mammal'

    assert that(animals).in_each("attributes['class']").matches('mammal')
    assert that(animals).in_each("attributes['class']"). \
           matches(['mammal','mammal','mammal','mammal','mammal'])

    assert that(animals).in_each("attributes['kind']"). \
           matches(['dog','cat','cow','cow','cow'])

    try:
        assert that(animals).in_each("attributes['kind']").matches(['dog'])
        assert False, 'should not reach here'
    except AssertionError, e:
        assert that(unicode(e)).equals(
            '%r has 5 items, but the matching list has 1: %r' % (
                ['dog','cat','cow','cow','cow'], ['dog'],
            )
        )


def test_that_raises():
    "sure.that(callable, with_args=[arg1], and_kwargs={'arg2': 'value'}).raises(SomeException)"

    called = False
    global called

    def function(arg1=None, arg2=None):
        global called
        called = True
        if arg1 == 1 and arg2 == 2:
            raise RuntimeError('yeah, it failed')

        return "OK"

    try:
        function(1, 2)
        assert False, 'should not reach here'

    except RuntimeError, e:
        assert unicode(e) == 'yeah, it failed'

    except Exception:
        assert False, 'should not reach here'

    finally:
        assert called
        called = False

    assert_raises(RuntimeError, function, 1, 2)

    called = False
    assert_equals(function(3, 5), 'OK')
    assert called

    called = False
    assert that(function, with_args=[1], and_kwargs={'arg2': 2}). \
           raises(RuntimeError)
    assert called

    called = False
    assert that(function, with_args=[1], and_kwargs={'arg2': 2}). \
           raises(RuntimeError, 'yeah, it failed')
    assert called

    called = False
    assert that(function, with_args=[1], and_kwargs={'arg2': 2}). \
           raises('yeah, it failed')
    assert called

    called = False
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}). \
           raises(RuntimeError)
    assert called

    called = False
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}). \
           raises(RuntimeError, 'yeah, it failed')
    assert called

    called = False
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}). \
           raises('yeah, it failed')
    assert called

    called = False
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}). \
           raises(r'it fail')
    assert called

    called = False
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}). \
           raises(RuntimeError, r'it fail')
    assert called


def test_that_looks_like():
    "sure.that('String\\n with BREAKLINE').looks_like('string with breakline')"
    assert that('String\n with BREAKLINE').looks_like('string with breakline')


def test_that_raises_with_args():
    "sure.that(callable, with_args=['foo']).raises(FooError)"

    class FooError(Exception):
        pass

    def my_function(string):
        if string == 'foo':
            raise FooError('OOps')

    assert that(my_function, with_args=['foo']).raises(FooError, 'OOps')


def test_that_does_not_raise_with_args():
    "sure.that(callable).doesnt_raise(FooError) and does_not_raise"

    class FooError(Exception):
        pass

    def my_function(string):
        if string == 'foo':
            raise FooError('OOps')

    assert that(my_function, with_args=['foo']).raises(FooError, 'OOps')


def test_that_contains_string():
    "sure.that('foobar').contains('foo')"

    assert 'foo' in 'foobar'
    assert that('foobar').contains('foo')


def test_that_doesnt_contain_string():
    "sure.that('foobar').does_not_contain('123'), .doesnt_contain"

    assert '123' not in 'foobar'
    assert that('foobar').doesnt_contain('123')
    assert that('foobar').does_not_contain('123')


def test_that_contains_none():
    "sure.that('foobar').contains(None)"

    try:
        assert that('foobar').contains(None)
        assert False, 'should not reach here'
    except Exception, e:
        assert_equals(
            unicode(e),
            u"'in <string>' requires string as left operand, not NoneType",
        )


def test_that_none_contains_string():
    "sure.that(None).contains('bungalow')"

    try:
        assert that(None).contains('bungalow')
        assert False, 'should not reach here'
    except Exception, e:
        assert_equals(
            unicode(e),
            u"argument of type 'NoneType' is not iterable",
        )


def test_that_some_iterable_is_empty():
    "sure.that(some_iterable).is_empty and sure.that(something).are_empty"

    assert that([]).is_empty
    assert that([]).are_empty

    assert that(tuple()).is_empty
    assert that({}).are_empty

    def fail_single():
        assert that((1,)).is_empty

    assert that(fail_single).raises('(1,) is not empty, it has 1 item')

    def fail_plural():
        assert that((1, 2)).is_empty

    assert that(fail_plural).raises('(1, 2) is not empty, it has 2 items')


def test_that_something_is_empty_raises():
    "sure.that(something_not_iterable).is_empty and sure.that(something_not_iterable).are_empty raises"

    obj = object()

    def fail():
        assert that(obj).is_empty
        assert False, 'should not reach here'

    assert that(fail).raises('%r is not iterable' % obj)


def test_that_something_iterable_matches_another():
    "sure.that(something_iterable).matches(another_iterable)"

    KlassOne = type('KlassOne', (object,), {})
    KlassTwo = type('KlassTwo', (object,), {})
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
        assert that(range(1)).matches(xrange(2))

    class Fail2(object):
        def __init__(self):
            assert that(xrange(1)).equals(range(2))

    class Fail3(object):
        def __call__(self):
            assert that(xrange(1)).equals(range(2))

    assert that(fail_1).raises('[0] has 1 item, but xrange(2) has 2 items')
    assert that(Fail2).raises('xrange(1) has 1 item, but [0, 1] has 2 items')
    assert that(Fail3()).raises('xrange(1) has 1 item, but [0, 1] has 2 items')


def test_within_pass():
    "within(five=miliseconds) will pass"
    from sure import within, miliseconds

    within(five=miliseconds)(lambda *a: None)()


def test_within_fail():
    "within(five=miliseconds) will fail"
    import time
    from sure import within, miliseconds

    def sleepy():
        time.sleep(0.7)

    failed = False
    try:
        within(five=miliseconds)(sleepy)()
    except AssertionError, e:
        failed = True
        assert_equals('sleepy did not run within five miliseconds', str(e))

    assert failed, 'within(five=miliseconds)(sleepy) did not fail'


def test_word_to_number():
    assert_equals(sure.word_to_number('one'),      1)
    assert_equals(sure.word_to_number('two'),      2)
    assert_equals(sure.word_to_number('three'),    3)
    assert_equals(sure.word_to_number('four'),     4)
    assert_equals(sure.word_to_number('five'),     5)
    assert_equals(sure.word_to_number('six'),      6)
    assert_equals(sure.word_to_number('seven'),    7)
    assert_equals(sure.word_to_number('eight'),    8)
    assert_equals(sure.word_to_number('nine'),     9)
    assert_equals(sure.word_to_number('ten'),     10)
    assert_equals(sure.word_to_number('eleven'),  11)
    assert_equals(sure.word_to_number('twelve'),  12)


def test_word_to_number_fail():
    failed = False
    try:
        sure.word_to_number('twenty')
    except AssertionError, e:
        failed = True
        assert_equals(
            unicode(e),
            'sure supports only literal numbers from one ' \
            'to twelve, you tried the word "twenty"')

    assert failed, 'should raise assertion error'


def test_microsecond_unit():
    "testing microseconds convertion"
    cfrom, cto = sure.UNITS[sure.microsecond]

    assert_equals(cfrom(1), 100000)
    assert_equals(cto(1), 1)

    cfrom, cto = sure.UNITS[sure.microseconds]

    assert_equals(cfrom(1), 100000)
    assert_equals(cto(1), 1)


def test_milisecond_unit():
    "testing miliseconds convertion"
    cfrom, cto = sure.UNITS[sure.milisecond]

    assert_equals(cfrom(1), 1000)
    assert_equals(cto(100), 1)

    cfrom, cto = sure.UNITS[sure.miliseconds]

    assert_equals(cfrom(1), 1000)
    assert_equals(cto(100), 1)


def test_second_unit():
    "testing seconds convertion"
    cfrom, cto = sure.UNITS[sure.second]

    assert_equals(cfrom(1), 1)
    assert_equals(cto(100000), 1)

    cfrom, cto = sure.UNITS[sure.seconds]

    assert_equals(cfrom(1), 1)
    assert_equals(cto(100000), 1)


def test_minute_unit():
    "testing minutes convertion"
    cfrom, cto = sure.UNITS[sure.minute]

    assert_equals(cfrom(60), 1)
    assert_equals(cto(1), 6000000)

    cfrom, cto = sure.UNITS[sure.minutes]

    assert_equals(cfrom(60), 1)
    assert_equals(cto(1), 6000000)


def test_within_pass_utc():
    "within(five=miliseconds) gives utc parameter"
    from sure import within, miliseconds
    from datetime import datetime

    def assert_utc(utc):
        assert isinstance(utc, datetime)

    within(five=miliseconds)(assert_utc)()


def test_that_is_a_matcher_should_absorb_callables_to_be_used_as_matcher():
    u"that.is_a_matcher should absorb callables to be used as matcher"
    @that.is_a_matcher
    def is_truthful(what):
        assert bool(what), '{0} is so untrue'.format(what)
        return 'foobar'

    assert that('friend').is_truthful()
    assert_equals(that('friend').is_truthful(), 'foobar')


def test_accepts_setup_list():
    "sure.with_context() accepts a list of callbacks for setup"

    def setup1(context):
        context.first_name = "John"

    def setup2(context):
        context.last_name = "Resig"

    @sure.that_with_context([setup1, setup2])
    def john_is_within_context(context):
        assert context.first_name == 'John'
        assert context.last_name == 'Resig'

    john_is_within_context()
    assert_equals(
        john_is_within_context.__name__,
        'john_is_within_context',
    )


def test_accepts_teardown_list():
    "sure.with_context() runs teardown before the function itself"

    class something:
        modified = True
        finished = 'nope'

    def setup(context):
        something.modified = False

    def teardown1(context):
        something.modified = True

    def teardown2(context):
        something.finished = 'yep'

    @sure.that_with_context(setup, [teardown1, teardown2])
    def something_was_modified(context):
        assert not something.modified
        assert something.finished == 'nope'

    something_was_modified()
    assert something.modified
    assert something.finished == 'yep'


def test_scenario_is_alias_for_context_on_setup_and_teardown():
    "@scenario aliases @that_with_context for setup and teardown"
    from sure import scenario

    def setup(context):
        context.name = "Robert C Martin"

    def teardown(context):
        assert_equals(context.name, "Robert C Martin")

    @scenario([setup], [teardown])
    def robert_is_within_context(context):
        "Robert is within context"
        assert isinstance(context, VariablesBag)
        assert hasattr(context, "name")
        assert_equals(context.name, "Robert C Martin")

    robert_is_within_context()
    assert_equals(
        robert_is_within_context.__name__,
        'robert_is_within_context',
    )


def test_actions_returns_context():
    "the actions always returns the context"
    from sure import action_for, that, scenario

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
    from sure import action_for, scenario

    def with_setup(context):
        @action_for(context, provides=['var1', 'foobar'])
        def the_context_has_variables():
            context.var1 = 123
            context.foobar = "qwerty"

    @scenario(with_setup)
    def the_providers_are_working(Then):
        Then.the_context_has_variables()
        assert hasattr(Then, 'var1')
        assert hasattr(Then, 'foobar')
        assert hasattr(Then, '__sure_providers_of__')

        providers = Then.__sure_providers_of__
        action = Then.the_context_has_variables.__name__

        providers_of_var1 = [p.__name__ for p in providers['var1']]
        assert that(providers_of_var1).contains(action)

        providers_of_foobar = [p.__name__ for p in providers['foobar']]
        assert that(providers_of_foobar).contains(action)

        return True

    assert the_providers_are_working()


def test_fails_when_action_doesnt_fulfill_the_agreement_of_provides():
    "it fails when an action doesn't fulfill its agreements"
    from sure import action_for, scenario

    error = 'the action "bad_action" was supposed to provide the ' \
        'attribute "two" into the context, but it did not. Please ' \
        'double check its implementation'

    def with_setup(context):
        @action_for(context, provides=['one', 'two'])
        def bad_action():
            context.one = 123

    @scenario(with_setup)
    def the_providers_are_working(the):
        assert that(the.bad_action).raises(AssertionError, error)
        return True

    assert the_providers_are_working()


def test_depends_on_failing_due_nothing_found():
    "it fails when an action depends on some attribute that is not " \
        "provided by any other previous action"
    import os
    from sure import action_for, scenario

    fullpath = os.path.abspath(__file__)
    error = 'the action "lonely_action" defined at %s:901 ' \
        'depends on the attribute "something" to be available in the' \
        ' context. It turns out that there are no actions providing ' \
        'that. Please double-check the implementation' % fullpath

    def with_setup(context):
        @action_for(context, depends_on=['something'])
        def lonely_action():
            pass

    @scenario(with_setup)
    def depends_on_fails(the):
        assert that(the.lonely_action).raises(AssertionError, error)
        return True

    assert depends_on_fails()


def test_depends_on_failing_due_not_calling_a_previous_action():
    "it fails when an action depends on some attribute that is being " \
        "provided by other actions"

    import os
    from sure import action_for, scenario

    fullpath = os.path.abspath(__file__)
    error = 'the action "my_action" defined at {0}:931 ' \
        'depends on the attribute "some_attr" to be available in the context.'\
        ' You need to call one of the following actions beforehand:\n' \
        ' -> dependency_action at {0}:927'.format(fullpath)

    def with_setup(context):
        @action_for(context, provides=['some_attr'])
        def dependency_action():
            context.some_attr = True

        @action_for(context, depends_on=['some_attr'])
        def my_action():
            pass

    @scenario(with_setup)
    def depends_on_fails(the):
        assert that(the.my_action).raises(AssertionError, error)
        return True

    assert depends_on_fails()


def test_that_contains_dictionary_keys():
    "sure.that(dict(name='foobar')).contains('name')"

    data = dict(name='foobar')
    assert 'name' in data
    assert 'name' in data.keys()
    assert that(data).contains('name')


def test_that_contains_list():
    "sure.that(['foobar', '123']).contains('foobar')"

    data = ['foobar', '123']
    assert 'foobar' in data
    assert that(data).contains('foobar')


def test_that_contains_set():
    "sure.that(set(['foobar', '123']).contains('foobar')"

    data = set(['foobar', '123'])
    assert 'foobar' in data
    assert that(data).contains('foobar')


def test_that_contains_tuple():
    "sure.that(('foobar', '123')).contains('foobar')"

    data = ('foobar', '123')
    assert 'foobar' in data
    assert that(data).contains('foobar')


def test_variables_bag_provides_meaningful_error_on_nonexisting_attribute():
    "VariablesBag() provides a meaningful error when attr does not exist"

    context = VariablesBag()

    context.name = "John"
    context.foo = "bar"

    assert that(context.name).equals("John")
    assert that(context.foo).equals("bar")

    def access_nonexisting_attr():
        assert context.bleh == 'crash :('

    assert that(access_nonexisting_attr).raises(
        AssertionError,
        'you have tried to access the attribute "bleh" from the context ' \
        '(aka VariablesBag), but there is no such attribute assigned to it. ' \
        'Maybe you misspelled it ? Well, here are the options: ' \
        '[\'name\', \'foo\']',
    )


def test_actions_providing_dinamically_named_variables():
    "the actions should be able to declare the variables they provide"
    from sure import action_for, scenario

    def with_setup(context):
        @action_for(context, provides=['var1', '{0}'])
        def the_context_has_variables(first_arg):
            context.var1 = 123
            context[first_arg] = "qwerty"

    @scenario(with_setup)
    def the_providers_are_working(Then):
        Then.the_context_has_variables('JohnDoe')
        assert hasattr(Then, 'var1')
        assert 'JohnDoe' in Then
        assert hasattr(Then, '__sure_providers_of__')

        providers = Then.__sure_providers_of__
        action = Then.the_context_has_variables.__name__

        providers_of_var1 = [p.__name__ for p in providers['var1']]
        assert that(providers_of_var1).contains(action)

        providers_of_JohnDoe = [p.__name__ for p in providers['JohnDoe']]
        assert that(providers_of_JohnDoe).contains(action)

        return True

    assert the_providers_are_working()


def test_deep_equals_dict_level1_success():
    "sure.that() deep_equals(dict) succeeding on level 1"

    something = {
        'one': 'yeah',
    }

    assert that(something).deep_equals({
        'one': 'yeah',
    })


def test_deep_equals_dict_level1_fail():
    "sure.that() deep_equals(dict) failing on level 1"

    something = {
        'one': 'yeah',
    }

    def assertions():
        assert that(something).deep_equals({
            'one': 'oops',
        })

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = {'one': 'yeah'}\n" \
        "    and\n" \
        "Y = {'one': 'oops'}\n" \
        "X['one'] is 'yeah' whereas Y['one'] is 'oops'",
    )


def test_deep_equals_list_level1_success():
    "sure.that(list) deep_equals(list) succeeding on level 1"

    something = ['one', 'yeah']
    assert that(something).deep_equals(['one', 'yeah'])


def test_deep_equals_list_level1_fail_by_value():
    "sure.that(list) deep_equals(list) failing on level 1"

    something = ['one', 'yeahs']

    def assertions():
        assert that(something).deep_equals(['one', 'yeah'])

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = ['one', 'yeahs']\n" \
        "    and\n" \
        "Y = ['one', 'yeah']\n" \
        "Y[1] is 'yeah' whereas should be like 'yeahs' as in X[1]",
    )


def test_deep_equals_list_level1_fail_by_length_x_gt_y():
    "sure.that(list) deep_equals(list) failing by length (len(X) > len(Y))"

    something = ['one', 'yeah', 'awesome!']

    def assertions():
        assert that(something).deep_equals(['one', 'yeah'])

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = ['one', 'yeah', 'awesome!']\n" \
        "    and\n" \
        "Y = ['one', 'yeah']\n" \
        "X has 3 items whereas Y has only 2",
    )


def test_deep_equals_list_level1_fail_by_length_y_gt_x():
    "sure.that(list) deep_equals(list) failing by length (len(Y) > len(X))"

    something = ['one', 'yeah']

    def assertions():
        assert that(something).deep_equals(['one', 'yeah', 'damn'])

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = ['one', 'yeah']\n" \
        "    and\n" \
        "Y = ['one', 'yeah', 'damn']\n" \
        "Y has 3 items whereas X has only 2",
    )


def test_deep_equals_dict_level1_fails_missing_key_on_y():
    "sure.that(X) deep_equals(Y) fails when Y is missing a key that X has"

    something = {
        'one': 'yeah',
    }

    def assertions():
        assert that(something).deep_equals({
            'two': 'yeah',
        })

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = {'one': 'yeah'}\n" \
        "    and\n" \
        "Y = {'two': 'yeah'}\n" \
        "X has the key \"one\" whereas Y doesn't",
    )


def test_deep_equals_failing_basic_vs_complex():
    "sure.that(X) deep_equals(Y) fails with basic vc complex type"

    def assertions():
        assert that('two yeah').deep_equals({
            'two': 'yeah',
        })

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = 'two yeah'\n"
        "    and\n" \
        "Y = {'two': 'yeah'}\n" \
        "X is a str and Y is a dict instead",
    )


def test_deep_equals_failing_complex_vs_basic():
    "sure.that(X) deep_equals(Y) fails with complex vc basic type"

    def assertions():
        assert that({'two': 'yeah'}).deep_equals('two yeah')

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = {'two': 'yeah'}\n" \
        "    and\n" \
        "Y = 'two yeah'\n"
        "X is a dict and Y is a str instead",
    )


def test_deep_equals_tuple_level1_success():
    "sure.that(tuple) deep_equals(tuple) succeeding on level 1"

    something = ('one', 'yeah')
    assert that(something).deep_equals(('one', 'yeah'))


def test_deep_equals_tuple_level1_fail_by_value():
    "sure.that(tuple) deep_equals(tuple) failing on level 1"

    something = ('one', 'yeahs')

    def assertions():
        assert that(something).deep_equals(('one', 'yeah'))

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = ('one', 'yeahs')\n" \
        "    and\n" \
        "Y = ('one', 'yeah')\n" \
        "Y[1] is 'yeah' whereas should be like 'yeahs' as in X[1]",
    )


def test_deep_equals_tuple_level1_fail_by_length_x_gt_y():
    "sure.that(tuple) deep_equals(tuple) failing by length (len(X) > len(Y))"

    something = ('one', 'yeah', 'awesome!')

    def assertions():
        assert that(something).deep_equals(('one', 'yeah'))

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = ('one', 'yeah', 'awesome!')\n" \
        "    and\n" \
        "Y = ('one', 'yeah')\n" \
        "X has 3 items whereas Y has only 2",
    )


def test_deep_equals_tuple_level1_fail_by_length_y_gt_x():
    "sure.that(tuple) deep_equals(tuple) failing by length (len(Y) > len(X))"

    something = ('one', 'yeah')

    def assertions():
        assert that(something).deep_equals(('one', 'yeah', 'damn'))

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = ('one', 'yeah')\n" \
        "    and\n" \
        "Y = ('one', 'yeah', 'damn')\n" \
        "Y has 3 items whereas X has only 2",
    )


def test_deep_equals_fallsback_to_generic_comparator():
    "sure.that() deep_equals(dict) falling back to generic comparator"
    from datetime import datetime
    now = datetime.now()
    something = {
        'one': 'yeah',
        'date': now,
    }

    assert that(something).deep_equals({
        'one': 'yeah',
        'date': now,
    })


def test_deep_equals_fallsback_to_generic_comparator_failing():
    "sure.that() deep_equals(dict) with generic comparator failing"
    from datetime import datetime
    now = datetime(2012, 3, 5)
    tomorrow = datetime(2012, 3, 6)
    something = {
        'date': now,
    }

    def assertions():
        assert that(something).deep_equals({
            'date': tomorrow,
        })

    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = {'date': datetime.datetime(2012, 3, 5, 0, 0)}\n" \
        "    and\n" \
        "Y = {'date': datetime.datetime(2012, 3, 6, 0, 0)}\n" \
        "X['date'] != Y['date']",
    )


def test_deep_equals_dict_level2_success():
    "sure.that() deep_equals(dict) succeeding on level 2"

    something = {
        'one': 'yeah',
        'another': {
            'two': 'cool',
        },
    }

    assert that(something).deep_equals({
        'one': 'yeah',
        'another': {
            'two': 'cool',
        },
    })


def test_deep_equals_dict_level2_list_success():
    "sure.that() deep_equals(dict) succeeding on level 2"

    something = {
        'one': 'yeah',
        'another': ['one', 'two', 3],
    }

    assert that(something).deep_equals({
        'one': 'yeah',
        'another': ['one', 'two', 3],
    })


def test_deep_equals_dict_level2_fail():
    "sure.that() deep_equals(dict) failing on level 2"

    something = {
        'one': 'yeah',
        'another': {
            'two': '##',
        },
    }

    def assertions():
        assert that(something).deep_equals({
            'one': 'yeah',
            'another': {
                'two': '$$',
            },
        })
    assert that(assertions).raises(
        AssertionError,
        "given\n" \
        "X = {'another': {'two': '##'}, 'one': 'yeah'}\n" \
        "    and\n" \
        "Y = {'another': {'two': '$$'}, 'one': 'yeah'}\n" \
        "X['another']['two'] is '##' whereas Y['another']['two'] is '$$'",
    )
