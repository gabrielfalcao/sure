.. _API-Reference:

API Reference
=============

``sure``
--------

.. py:module:: sure

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

.. autofunction:: sure.do_enable

.. autofunction:: sure.enable


``sure.core``
-------------

.. py:module:: sure.core

.. autoclass:: sure.core.DeepExplanation

.. autoclass:: sure.core.DeepComparison

.. autofunction:: sure.core._get_file_name

.. autofunction:: sure.core._get_line_number

.. autofunction:: sure.core.itemize_length


``sure.runner``
---------------

.. py:module:: sure.runner

.. autoclass:: sure.runner.Runner

``sure.loader``
-----------------

.. py:module:: sure.loader

.. autofunction:: sure.loader.resolve_path

.. autofunction:: sure.loader.get_root_python_module

.. autoclass:: sure.loader.loader


``sure.reporter``
---------------------

.. py:module:: sure.reporter

.. autoclass:: sure.reporter.Reporter


``sure.reporters``
------------------

.. py:module:: sure.reporters

.. autoclass:: sure.reporters.feature.FeatureReporter


``sure.original``
-----------------

.. py:module:: sure.original

.. autofunction:: sure.original.identify_callable_location

.. autofunction:: sure.original.is_iterable

.. autofunction:: sure.original.all_integers

.. autofunction:: sure.original.explanation
