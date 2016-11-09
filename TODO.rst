TODO
~~~~

New way for adding behavior to scenarios


.. code:: python

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
