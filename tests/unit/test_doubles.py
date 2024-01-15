# -*- coding: utf-8 -*-
# <sure - sophisticated automated test library and runner>
# Copyright (C) <2010-2024>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"unit tests for :mod:`sure.doubles`"

from sure import expects
from sure.doubles.dummies import Dummy, anything_of_type, AnythingOfType
from sure.doubles.fakes import FakeOrderedDict
from sure.doubles.stubs import stub


class AutoMobile(object):
    def __init__(self, model: str, manufacturer: str, year: int, color: str, features: dict):
        self.model = model
        self.year = year
        self.color = color


def test_stub():
    ":func:`sure.doubles.stubs.stub` should create a stub with the given type and keyword-args"

    veraneio = stub(
        AutoMobile,
        model="Omega",
        manufacturer="Chevrolet",
        year=1993,
        color="Graphite",
    )
    expects(veraneio).to.be.an(AutoMobile)
    expects(veraneio).to.have.property("year").being.equal(1993)
    expects(veraneio).to.have.property("model").being.equal("Omega")
    expects(veraneio).to.have.property("color").being.equal("Graphite")
    expects(veraneio).to.have.property("manufacturer").being.equal("Chevrolet")


def test_stub_without_base_class():
    ":func:`sure.doubles.stubs.stub` should create an opaque object when not providing a `base_class' param"

    auto = stub(
        model="Opala",
        manufacturer="Chevrolet",
        year=71,
        color="White",
        features={"vinyl_roof": "black"},
    )
    expects(auto).to.have.property("model").being.equal("Opala")
    expects(auto).to.have.property("manufacturer").being.equal("Chevrolet")
    expects(auto).to.have.property("color").being.equal("White")


def test_fake_ordered_dict_str():
    ":meth:`sure.doubles.fakes.FakeOrderedDict.__str__` should be similar to that of :meth:`dict.__str__`"

    fake_ordered_dict = FakeOrderedDict([("a", "A"), ("z", "Z")])
    expects(str(fake_ordered_dict)).to.equal("{'a': 'A', 'z': 'Z'}")
    expects(str(FakeOrderedDict())).to.equal("{}")


def test_fake_ordered_dict_repr():
    ":meth:`sure.doubles.fakes.FakeOrderedDict.__repr__` should be similar to that of :meth:`dict.__repr__`"

    fake_ordered_dict = FakeOrderedDict([("a", "A"), ("z", "Z")])
    expects(repr(fake_ordered_dict)).to.equal("{'a': 'A', 'z': 'Z'}")
    expects(repr(FakeOrderedDict())).to.equal("{}")


def test_dummy():
    "Dummy() should return the dummy_id"

    dummy = Dummy("some dummy id")
    expects(dummy).to.have.property("__dummy_id__").being.equal("some dummy id")

    expects(str(dummy)).to.equal("<Dummy some dummy id>")
    expects(repr(dummy)).to.equal("<Dummy some dummy id>")


def test_dummy_takes_exclusively_string_as_id():
    "Dummy() should throw exception when receiving a non-string param"

    expects(Dummy).when.called_with(299).should.throw(
        TypeError,
        "sure.doubles.dummies.Dummy() takes string as argument, received 299 (<class 'int'>) instead",
    )


def test_anything_of_type_should_return_an_instance_of_the_anythingoftype_class():
    "anything_of_type() should return an instance of the AnythingOfType class"

    expects(anything_of_type(str)).to.be.an(AnythingOfType)
    expects(str(anything_of_type(str))).to.equal(
        "<AnythingOfType[builtins.str] anything_of_type(builtins.str)>"
    )
    expects(repr(anything_of_type(str))).to.equal(
        "<AnythingOfType[builtins.str] anything_of_type(builtins.str)>"
    )


def test_anything_of_type_should_equal_any_python_object_of_the_given_type():
    "anything_of_type() should return ``True`` for the :func:`operator.eq`"

    expects(anything_of_type(str) == "anything_of_type(str)").to.not_be.false
    expects(anything_of_type(str)).to.equal("anything_of_type(str)")

    expects(anything_of_type(str) == b"anything_of_type(str)").to.be.false
    expects(anything_of_type(str)).to_not.equal(b"anything_of_type(str)")


def test_anything_of_type_should_raise_type_error_when_receiving_a_nontype_type_instance():
    'anything_of_type() should raise :exc:`TypeError` when receiving a non-type type "instance"'

    expects(anything_of_type).when.called_with("anything_of_type(str)").to.have.raised(
        TypeError,
        "'anything_of_type(str)' should be a class but is a <class 'str'> instead",
    )
