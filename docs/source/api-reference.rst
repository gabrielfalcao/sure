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

``sure.importer``
-----------------

.. py:module:: sure.importer

.. autofunction:: sure.importer.resolve_path

.. autofunction:: sure.importer.get_root_python_module

.. autoclass:: sure.importer.importer


``sure.reporter``
---------------------

.. py:module:: sure.reporter

.. autoclass:: sure.reporter.Reporter


``sure.reporters``
------------------

.. py:module:: sure.reporters

.. autoclass:: sure.reporters.feature.FeatureReporter


``sure.old``
------------

.. py:module:: sure.old

.. autofunction:: sure.old.identify_callable_location

.. autofunction:: sure.old.is_iterable

.. autofunction:: sure.old.all_integers

.. autofunction:: sure.old.explanation
