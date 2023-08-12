TODO
----


Test Runner
~~~~~~~~~~~

Pytest is unnecessarily verbose, showing full tracebacks when sure
already performs that at the lowest level rather than hijacking some
features of the python runtime.

Sure's prerrogative is that it's designed to empower engineers to
write adequate code rather than play with the language so as to
deliver "production" code without worrying so much about the test
runtime being diffrent than the production runtime.

The test runner should be simple enough like nosetests was, but don't
try to share too much information with the developer that might only
slow down one's developer project.


``.when.py2.should.`` and ``.should.when.py2.``
``.when.py3.should.`` and ``.should.when.py3.``


Mock and Stubbing support
~~~~~~~~~~~~~~~~~~~~~~~~~

New way for adding behavior to scenarios


.. code:: python

   import sure
   from sure.scenario import BehaviorDefinition

   class Example1(BehaviorDefinition):
       context_namespace = 'example1'

       def setup(self, argument1):
           self.data = {
               'parameter': argument1
           }

       def teardown(self):
           self.data = {}


   @apply_behavior(Example1, argument1='hello-world')
   def test_example_1(context):
       context.example1.data.should.equal({
           'parameter': 'hello-world',
       })
