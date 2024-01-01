.. _API-Reference:

API Reference
=============

``sure``
--------

.. automodule:: sure
.. autofunction:: sure.enable_special_syntax
.. autoclass:: sure.VariablesBag
.. autoclass:: sure.CallBack
.. autofunction:: sure.that_with_context
.. autofunction:: sure.within
.. autofunction:: sure.word_to_number
.. autofunction:: sure.assertionmethod
.. autofunction:: sure.assertionproperty
.. autoclass:: sure.IdentityAssertion
.. autoclass:: sure.AssertionBuilder
.. autofunction:: sure.assertion
.. autofunction:: sure.chain
.. autofunction:: sure.chainproperty
.. autoclass:: sure.ensure


``sure.core``
-------------

.. automodule:: sure.core
.. autoclass:: sure.core.DeepExplanation
.. _deep comparison:
.. autoclass:: sure.core.DeepComparison
.. autofunction:: sure.core.itemize_length


``sure.runner``
---------------

.. py:module:: sure.runner
.. autoclass:: sure.runner.Runner


``sure.loader``
-----------------

.. py:module:: sure.loader
.. autoclass:: sure.loader.loader
.. autofunction:: sure.loader.resolve_path
.. autofunction:: sure.loader.get_package
.. autofunction:: sure.loader.name_appears_to_indicate_test
.. autofunction:: sure.loader.appears_to_be_test_class
.. autofunction:: sure.loader.read_file_from_path


``sure.reporter``
-----------------

.. py:module:: sure.reporter
.. autoclass:: sure.reporter.Reporter

``sure.reporters``
------------------

.. py:module:: sure.reporters
.. autoclass:: sure.reporters.feature.FeatureReporter


``sure.original``
-----------------

.. automodule:: sure.original
.. autofunction:: sure.original.identify_callable_location
.. autofunction:: sure.original.is_iterable
.. autofunction:: sure.original.all_integers
.. autofunction:: sure.original.explanation

``sure.doubles``
----------------

.. automodule:: sure.doubles
.. autofunction:: sure.doubles.stub
.. autoclass:: sure.doubles.FakeOrderedDict
.. autoattribute:: sure.doubles.anything


``sure.doubles.dummies``
------------------------

.. autoclass:: sure.doubles.dummies.Anything
.. autoattribute:: sure.doubles.dummies.anything

``sure.doubles.fakes``
----------------------

.. automodule:: sure.doubles.fakes
.. autoclass:: sure.doubles.fakes.FakeOrderedDict

``sure.doubles.stubs``
----------------------

.. automodule:: sure.doubles.stubs
.. autoclass:: sure.doubles.stubs.stub
