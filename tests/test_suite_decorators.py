from sure.decorators import describe, given, when, then
from sure.suites import Scenario, TemporarySuiteVars



@describe('@describe() should describe a Scenario')
def should_describe_a_scenario(scenario, shared):
    scenario.should.be.a(Scenario)
    shared.should.be.a(TemporarySuiteVars)

    shared.some_value = None



@given("that `some_value` is 123")
def given_a_test_case(scenario, shared):

    shared.some_value.should.be.none
    shared.some_value = "123"


@when("I set the value to 456"):
def when_set_the_value(scenario, shared):

    shared.some_value.should.equal("123")
    shared.some_value = "456"


@when("Then it should be 456"):
def then_it_should_be_set(scenario, shared):

    shared.some_value.should.equal("123")
    shared.some_value = "456"



should_describe_a_scenario(
    given_a_test_case,
    when_set_the_value,
    then_it_should_be_set,
).run()
