TODO
----

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
