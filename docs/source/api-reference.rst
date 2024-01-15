.. _API-Reference:

API Reference
=============

``sure``
--------

.. automodule:: sure
.. autofunction:: sure.enable_special_syntax
.. autoclass:: sure.StagingArea
.. autoclass:: sure.CallBack
.. autofunction:: sure.scenario
.. autofunction:: sure.within
.. autofunction:: sure.word_to_number
.. autofunction:: sure.assertionmethod
.. autofunction:: sure.assertionproperty
.. autoclass:: sure.ObjectIdentityAssertion
.. autoclass:: sure.AssertionBuilder
.. autofunction:: sure.assertion
.. autofunction:: sure.chain
.. autofunction:: sure.chainproperty
.. autoclass:: sure.ensure


``sure.core``
-------------

.. automodule:: sure.core
.. autoclass:: sure.core.Explanation
.. _deep comparison:
.. autoclass:: sure.core.DeepComparison
.. autofunction:: sure.core.itemize_length


``sure.runner``
---------------

.. automodule:: sure.runner
.. autoclass:: sure.runner.Runner


``sure.loader``
---------------

.. automodule:: sure.loader
.. autoclass:: sure.loader.loader
.. autofunction:: sure.loader.resolve_path
.. autofunction:: sure.loader.get_package
.. autofunction:: sure.loader.get_type_definition_filename_and_firstlineno


``sure.loader.astutil``
-----------------------

.. automodule:: sure.loader.astutil
.. autofunction:: sure.loader.astutil.is_classdef
.. autofunction:: sure.loader.astutil.resolve_base_names
.. autofunction:: sure.loader.astutil.gather_class_definitions_node
.. autofunction:: sure.loader.astutil.gather_class_definitions_from_module_path


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
.. autofunction:: sure.original.identify_caller_location
.. autofunction:: sure.original.is_iterable
.. autofunction:: sure.original.all_integers
.. autofunction:: sure.original.explanation

``sure.doubles``
----------------

.. automodule:: sure.doubles
.. autofunction:: sure.doubles.stub
.. autoclass:: sure.doubles.FakeOrderedDict
.. autoattribute:: sure.doubles.dummies.anything


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
