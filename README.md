# sure
> Version 0.2

# What

a assertion toolbox that works fine with [nose](http://code.google.com/p/python-nose/)

# Install

    user@machine:~$ [sudo] pip install sure

# Documentation

## testing behaviour of objects

    from sure import that

    assert that("something").is_a(str)
    assert that("something").like("some")
    assert "thing" in that("something")

    class FooBar:
        attribute_one = "simple"

    assert "attribute_one" in that(FooBar)
    assert that(FooBar).equals(FooBar)

    # and so on ...

## strings

    from sure import that

    assert that("   string \n with    lots of \n spaces and breaklines\n\n ")
        .looks_like("string with lots of spaces and breaklines")

    assert that('foobar').contains('foo')

## iterable objects


### testing length

    from sure import that

    animals = ['dog', 'cat', 'chicken']
    objects = ['television', 'refrigerator']
    movies = ['conan', 'matrix', 'fight club', 'rocky', 'rambo']

    assert that([]).is_empty
    assert that([]).are_empty

    assert that(animals).len_is(3)
    assert that(animals).len_is(['list with', 'three', 'elements'])

    assert that(movies).len_greater_than(3)
    assert that(movies).len_greater_than(animals)
    assert that(movies).len_greater_than(objects)

    assert that(movies).len_greater_than(3)
    assert that(movies).len_greater_than(animals)
    assert that(movies).len_greater_than(objects)

    assert that(movies).len_greater_than_or_equals(3)
    assert that(movies).len_greater_than_or_equals(animals)
    assert that(movies).len_greater_than_or_equals(objects)

    assert that(objects).len_lower_than(3)
    assert that(objects).len_lower_than(animals)
    assert that(objects).len_lower_than(objects)

    assert that(objects).len_lower_than_or_equals(3)
    assert that(objects).len_lower_than_or_equals(animals)
    assert that(objects).len_lower_than_or_equals(objects)

### testing elements

    from sure import that

    class Animal:
      def __init__(self, name):
        self.kind = 'mammal'
        self.name = name

    mammals = [
      Animal('dog'),
      Animal('cat'),
      Animal('cat'),
      Animal('cow'),
    }

    assert that(mammals).the_attribute('kind').equals('mammal')
    assert that(mammals, within_range(1, 2)).the_attribute('name').equals('cat')

#### further

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

    assert that(animals).in_each("attributes['class']").matches('mammal')
    assert that(animals).in_each("attributes['class']").matches(['mammal','mammal','mammal','mammal','mammal'])

    assert that(animals).in_each("attributes['kind']").matches(['dog','cat','cow','cow','cow'])

## contextual setup and teardown

    import sure

    def setup_file(context):
        context.file = open("foobar.xml")

    def teardown_file(context):
        context.file.close()

    @sure.that_with_context(setup_file, teardown_file):
    def file_is_a_xml(context):
        "this the file is a xml"
        sure.that(context.file.read()).contains("<root>")


    # and so on ...

## timed tests

    from sure import *

    @within(five=seconds):
    def test_sleep_for_4_seconds():
        import time
        time.sleep(4)

    @within(ten=miliseconds):
    def test_sleep_for_4_miliseconds():
        import time
        time.sleep(0.004)

    @within(ten=microseconds):
    def test_sleep_for_12_microseconds():
        import time
        time.sleep(0.00012)

    @within(one=minute):
    def test_sleep_for_59_seconds():
        import time
        time.sleep(59)

    @within(two=minutes):
    def test_sleep_for_1_minute_and_59_seconds():
        import time
        time.sleep(119)

if any of the tests above take more than expected, a assertion_error is raised

## exceptions

    def function(arg1=None, arg2=None):
        if arg1 and arg2:
            raise RuntimeError('yeah, it failed')

    assert that(function, with_args=[1], and_kwargs={'arg2': 2}).raises(RuntimeError)
    assert that(function, with_args=[1], and_kwargs={'arg2': 2}).raises(RuntimeError, 'yeah, it failed')
    assert that(function, with_args=[1], and_kwargs={'arg2': 2}).raises('yeah, it failed')

    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}).raises(RuntimeError)
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}).raises(RuntimeError, 'yeah, it failed')
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}).raises('yeah, it failed')

    # you can also match pieces of the string
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}).raises('it failed')
    assert that(function, with_kwargs={'arg1': 1, 'arg2': 2}).raises(RuntimeError, 'it failed')

# license

sure is under MIT license, so that it can be embedded into your
project, and ran within your sandbox.

    Copyright (C) <2010>  Gabriel Falcão <gabriel@nacaolivre.org>

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.
