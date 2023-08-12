[draft] Changes in version 1.5.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Introducing the concept of BehaviorDefinition: a clean and
  decoupled way to reutilize setup/teardown behaviors. So instead of
  the classic massive setup/teardown methods and/or chaotic
  ``unittest.TestCase`` subclass inheritance every test can be
  decorated with @apply_behavior(CustomBehaviorDefinitionTypeObject)

* Avoid using the word "test" in your "Behavior Definitions" so that
  nose will not mistake your BehaviorDefinition with an actual test
  case class and thus execute .setup() and .teardown() in an
  undesired manner.
