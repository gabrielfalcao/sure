# sure
> Version 0.7.0

# What

a assertion toolbox that works fine with [nose](http://code.google.com/p/python-nose/)

# Install

    user@machine:~$ [sudo] pip install sure

# Documentation

## testing behaviour of objects

```python
from sure import that

assert that("something").is_a(str)
assert that("something").like("some")
assert "thing" in that("something")

class FooBar:
    attribute_one = "simple"

assert "attribute_one" in that(FooBar)
assert that(FooBar).has("attribute_one")
assert that(FooBar).equals(FooBar)

# go faster

assert that(FooBar).at('attribute_one').equals('simple')

# and also for dictionaries

name = dict(john='doe')
assert that(name).has('john')

# go faster
assert that(name).at('john').equals('doe')
```

## strings

```python
from sure import that

assert that("   string \n with    lots of \n spaces and breaklines\n\n ")
    .looks_like("string with lots of spaces and breaklines")

assert that('foobar').contains('foo')
assert that('foobar').doesnt_contain("123")
assert that('foobar').does_not_contain("123")
```

## iterable objects


### testing length

```python
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
```

### testing elements

```python
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
```

#### further

```python
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
```

## contextual setup and teardown

```python
import sure

def setup_file(context):
    context.file = open("foobar.xml")

def teardown_file(context):
    context.file.close()

@sure.that_with_context(setup_file, teardown_file):
def file_is_a_xml(context):
    "this file is a xml"
    sure.that(context.file.read()).contains("<root>")
```

### you can also use lists containing callbacks for setup/teardown

Like this:

```python
def setup_file(context):
    context.file = open("foobar.xml")

def a_browser(context):
    from httplib2 import Http
    context.browser = Http()

def then_clean_file(context):
    context.file.close()

def and_browser(context):
    del context.browser

@sure.that_with_context([setup_file, a_browser], [then_clean_file, and_browser]):
def file_equals_response(context):
    "the file equals the response"
    headers, response_body = context.http.request('http://github.com', 'GET')

    file_contents = context.file.read()
    sure.that(response_body).contains(file_contents)
```

## timed tests

```python
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
```

if any of the tests above take more than expected, a assertion_error is raised

## exceptions

```python
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
```

### testing if some callback should never raise an exception

```python
def good_boy():
    pass

assert that(good_boy).does_not_raise(Exception)
assert that(good_boy).doesnt_raise(Exception)

## add your own matchers

```python
@that.is_a_matcher
def could_work(matcher, parameter):
    assert matcher._src == "this"
    assert parameter == "I mean, for real!"
    return "cool!"

assert that("this").could_work("I mean, for real!") == "cool!"
```

# Go BDD with me :)

Sure aliases the decorator `@that_with_context` as `@scenario` and the
context passed as parameter is just a bag of variables you can mess
with. So that your scenario can share data in a really flexible way.

Aditionally, you can add actions through your setup functions and they
will last only for your scenario's lifetime.

## let's see it in action

```python
    from sure import action_in, that, scenario

    def with_setup(context):
        @action_in(context)
        def i_have_an_action(received_text):
            assert_equals(received_text, "yay, I do!")
            return "this pretty text"

    @scenario([with_setup])
    def i_can_use_actions(context):
        "We should be able to use actions"
        given = the = context
        given.i_have_an_action("yay, I do!").contextualized_as('value')

        assert that(the.value).equals("this pretty text")
        return True

    assert i_can_use_actions()
```

### action_in, action_for, all the same thing!

```python
def test_action_can_be_contextualized_aliased():
    "sure.action_for is an alias for sure.action_in"
    from sure import action_for, that, scenario

    def with_setup(context):
        @action_for(context)
        def i_have_an_action(received_text):
            assert_equals(received_text, "super cool")
            return "this other pretty text"

    @scenario([with_setup])
    def scenario_above(context):
        given = the = context
        given.i_have_an_action("super cool").contextualized_as('awesomeness')

        assert that(the.awesomeness).equals("this other pretty text")
        the.awesomeness = 'was amazing'
        return the['awesomeness']

    assert_equals(scenario_above(), 'was amazing')
```

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
