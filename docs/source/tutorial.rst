.. _Tutorial:

..
   WORK IN PROGRESS, please don't add this to the table of contents

How to organize your tests
==========================

Here is a proposal on how to organize your tests.
I have been using this manner of project organization

Python Testing: how to organize your project
forget about test cases, welcome scenarios


Pro tips
--------

Adding test coverage to existing code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* If your test needs to manually set a side-effect on the target
  object it means that you should write a method for your class that
  will perform the side-effect, then you can simply call a single
  method from your test.
