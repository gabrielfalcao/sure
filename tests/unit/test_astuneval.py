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
import ast
from sure import expects
from sure.astuneval import parse_body
from sure.astuneval import parse_accessor
from sure.astuneval import Accessor, NameAccessor, SubsAccessor, AttributeAccessor


def test_parse_body_against_several_kinds():
    expects(parse_body("atomic_bonds[3:7]")).to.be.an(ast.Subscript)
    expects(parse_body("children[6]")).to.be.an(ast.Subscript)
    expects(parse_body("hippolytus")).to.be.an(ast.Name)
    expects(parse_body("zone[4].damage")).to.be.an(ast.Attribute)


def test_parse_accessor_name_accessor():
    class Tragedy:
        telemachus = "♒️"

    expects(parse_accessor("telemachus")).to.be.a(NameAccessor)
    get_character = parse_accessor("telemachus")
    expects(get_character(Tragedy)).to.equal('♒️')


def test_parse_accessor_subscript_accessor():
    class MonacoGrandPrix1990:
        classification = [
            "Ayrton Senna",
            "Alain Prost",
            "Jean Alesi",
        ]
    expects(parse_accessor("classification[2]")).to.be.a(SubsAccessor)
    get_position = parse_accessor("classification[2]")
    expects(get_position(MonacoGrandPrix1990)).to.equal("Jean Alesi")


def test_parse_accessor_attr_accessor():
    class FirstResponder:
        def __init__(self, bound: str, damage: str):
            self.bound = bound
            self.damage = damage

    class Incident:
        first_responders = [
            FirstResponder("Wyckoff", "unknown"),
            FirstResponder("Beth Israel", "unknown"),
            FirstResponder("Brooklyn Hospital Center", "unknown"),
            FirstResponder("Woodhull", "administered wrong medication"),
        ]
    expects(parse_accessor("first_responders[3].damage")).to.be.a(AttributeAccessor)

    access_damage = parse_accessor("first_responders[3].damage")
    expects(access_damage(Incident)).to.equal("administered wrong medication")
