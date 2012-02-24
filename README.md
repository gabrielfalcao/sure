# sure
> Version 0.8.0

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
vassert that(FooBar).has("attribute_one")
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
```

## add your own matchers

```python
@that.is_a_matcher
def could_work(matcher, parameter):
    assert matcher._src == "this"
    assert parameter == "I mean, for real!"
    return "cool!"

assert that("this").could_work("I mean, for real!") == "cool!"
```

<a name="BDD" />
# Hipster BDD with just... python code

Unlikely [lettuce](http://lettuce.it), sure allows you to describe the
behavior you expect your application to have, very focused on
providing a very declarative and self-describing DSL through simple
tricks around the python syntax.

This may disagree with conventions like [PEP-8](http://www.python.org/dev/peps/pep-0008/) and Tim Peters's
[Zen of Python](http://www.python.org/dev/peps/pep-0020/).

It's not that "sure" disagrees with those conventions, the module
itself follows both PEP-8 and PEP-20. But it turns out that "sure"
provides you with sometimes conflicting conventions, for the sake of
readability and maintainability of the code that makes sure your
production code is always healthy.

Sure aliases the decorator `@that_with_context` as `@scenario` and the
context passed as parameter is just a bag of variables you can mess
around without feeling like juggling with machetes. So that your
scenario can share data in a really flexible way.

*Don't worry, "sure"'s internals seal the variables you use within the
 test scope and its setup/teardown functions. Everything is sandboxed.

## The idea

Firstly, if you are not familiar with [Behavior-driven development](http://antonymarcano.com/blog/2011/03/goals-tasks-action/) I strongly recommend the blog post ["What's in a story"](http://dannorth.net/whats-in-a-story/), by [Dan North](http://dannorth.net), former [ThoughtWorks](http://en.wikipedia.org/wiki/ThoughtWorks) employee. And as you might know, ThoughtWorks [is internationally recognized](http://en.wikipedia.org/wiki/ThoughtWorks#History) as being the cradle of agile methodologies, which often includes using assorted automated test engineering techniques.

Sure is pretty much just a layer you should use on top of
[nose-compatible test functions](http://readthedocs.org/docs/nose/en/latest/writing_tests.html#test-functions). It
provides you with decorators that leverage declaring scenarios and
actions to be executed within them.

The DSL itself is just python code, altough it requires a certain
effort from the developers that authors the tests. In the other hand,
it also provides builtin validation of action executions, looking for
conflicting inter-dependency, as well as giving very meaningful
feedback, so that you won't spend hours debugging messed up code.

## Nomenclature

There are a few small examples of usage through the sub-sections
below, don't rely solely on them, to go further on the API usage,
check the documentation.

### Scenario

Scenarios are actually just
[nose-compatible test functions](http://readthedocs.org/docs/nose/en/latest/writing_tests.html#test-functions)
decorated with `@scenario()`.

Scenarios accepts lists of callbacks that will be called before and after
themselves so that you have a fine grained setup/teardown management.
Also, scenarios will call the original test functions with one
argument: context

### Context

Context is a clever object that keeps records of its contents and
reporting ant problems when trying to access them, so that you know
what part of your test is wrong.

Contexts are also a key thing when calling actions, you can create
aliases of it named: `Given, When, Then, And` and so on... You can see
more in the examples or docs.

### Actions

Are the smalllest portions of test that will compose your actions,
declare them within any setup functions, the `@action_for` decorator
also gives you ways to explicit what variables the action will create
within the `context` argument, or require previous variables to be
already in the `context`.

This is one of the most important features of "sure", so that you and
your team will spend less time debugging a test and more on getting
things done.

### Setup/Teardown

As said above, the `@scenario()` decorators takes 2 positional
arguments: setup and teardown.  They can be both `callables` or `a
list of callables`.  This is specially useful when you wanna organize
your `Actions` into separated setup functions, then you only include
the ones you want in each scenario.

It may sound complicated, but during the rollout below you're gonna
see it's easy peasy.

#### !!! IMPORTANT NOTE ON SETUP/TEARDOWN !!!

Never, ever name your setup and teardown functions as just `setup` and
`teardown` respectivelly.  "Sure" has its own mechanism for calling
them with a context variable, but if you name the callbacks as `setup`
and/or `teardown`, then
[nose will call them manually](http://readthedocs.org/docs/nose/en/latest/writing_tests.html#fixtures),
but not only that: you will get a very bad error since the appropriate
`context` variable will not be passed as first argument.


## Examples

Let's go from a simple example and then we evolve into more features

## The simplest case

```python
from sure import action_for, that, scenario
from myapp import User

@scenario
def users_should_introduce_themselves(context):
    "Users should eb able to introduce themselves"

    # aliasing the context for semantic usage below
    Given = Then = context

    # defining some actions
    @action_for(context, provides=['user'])
    def there_is_a_user_called(name):
        context.user = User(first_name=name)

    @action_for(context, depends_on=['user'])
    def he_introduces_himself_with(a_greeting):
        assert that(context.user.say_hello()).looks_like(a_greeting)

    # calling the actions

    Given.there_is_a_user_called('Fabio')
    Then.he_introduces_himself_with('Hello, my name if Fabio. Nice meeting you')
```


## A slightly more elaborated example: browsing with django test client + lxml

```python
from django.test.client import Client
from lxml import html as lhtml
from sure import action_for, that, scenario

def prepare_browser(context):
    @action_in(context, provides=['browser', 'response', 'dom'])
    def I_navigate_to(path):
       # preparing the browser
       context.browser = Client()

       # saving the response
       context.response = context.browser.get(path)

       # also saving a DOM object for future traversing
       context.dom = lhtml.fromstring(context.response.content)

    @action_in(context, depends_on=['browser'], provides=['title'])
    def I_see_the_header_has_the_title(the_expected_title):
        # just saving the title for future use
        titles_found = context.dom.cssselect('header .title')

        assert that(titles_found).len_is(1)
        (context.title, ) = titles_found

        assert that(context.title.text).looks_like(the_expected_title)

    @action_in(context, depends_on=['title'])
    def the_title_also_has_the_classes(expected_classes):
        existing_classes = context.title.attrib.get('class', '')
        for expected_class in expected_classes:
            assert that(existing_classes).looks_like(expected_class)


@scenario([prepare_browser])
def navigate_to_index_page(context):
    "Navigate to the index page and check some HTML markup"
    Given = Then = context

    Given.I_navigate_to("/index")
    When.I_see_the_header_has_the_title("Welcome to our nifty website")
    Then.the_title_also_has_the_classes(["alert", "alert-info", "fade-in"])
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
