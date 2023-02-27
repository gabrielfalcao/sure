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


.. code:: python

   import sure


   def some_helper_function(value):
       if value == 'foo':
           return 'expected'


   def main_function_that_depends_on_helper(param1, param2):
       return some_helper_function(param1)


   def test_main_function_succeeds_when_helper_returns_expected_result():
       some_helper_function.stub.called_with('foo').returns(['expected'])

       result = main_function_that_depends_on_helper('foo', 'bar')

       result.should.equal('expected')
