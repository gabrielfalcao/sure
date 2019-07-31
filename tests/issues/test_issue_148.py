"""
Regression test for GitHub Issue #148
"""


def test_should_compare_dict_with_non_orderable_key_types():
    # given
    class Foo(object):
        def __eq__(self, other):
            return isinstance(other, Foo)

        def __hash__(self):
            return hash("Foo")

    class Bar(object):
        def __eq__(self, other):
            return isinstance(other, Bar)

        def __hash__(self):
            return hash("Bar")

    # when
    foo = Foo()
    bar = Bar()

    # then
    {foo: 0, bar: 1}.should.equal({foo: 0, bar: 1})


def test_should_compare_dict_with_enum_keys():
    try:
        from enum import Enum
    except ImportError:  # Python 2 environment
        # skip this test
        return

    # given
    class SomeEnum(Enum):
        A = 'A'
        B = 'B'

    # when & then
    {SomeEnum.A: 0, SomeEnum.B: 1}.should.equal({SomeEnum.A: 0, SomeEnum.B: 1})
