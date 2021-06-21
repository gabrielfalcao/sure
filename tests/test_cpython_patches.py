## #!/usr/bin/env python
# -*- coding: utf-8 -*-
# <sure - utility belt for automated testing in python>
# Copyright (C) <2010-2021>  Gabriel Falcão <gabriel@nacaolivre.org>
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
from __future__ import unicode_literals

import sure
from sure import expect
from sure.magic import is_cpython

# if is_cpython:
#     if sure.allows_new_syntax:

#         def test_it_works_with_objects():
#             ("anything that inherits from object should be patched")

#             (4).should.equal(2 + 2)
#             "foo".should.equal("f" + ("o" * 2))
#             {}.should.be.empty

#         def test_shouldnt_overwrite_class_attributes():
#             """do not patch already existing class attributes with same name"""

#             class Foo(object):
#                 when = 42
#                 shouldnt = 43
#                 bar = "bar"

#             Foo.when.should.be.equal(42)
#             Foo.shouldnt.should.be.equal(43)
#             Foo.bar.should.be.equal("bar")

#             Foo.__dict__.should.contain("when")
#             Foo.__dict__.should.contain("shouldnt")
#             Foo.__dict__.should.contain("bar")

#             dir(Foo).should.contain("when")
#             dir(Foo).should.contain("shouldnt")
#             dir(Foo).should.contain("bar")
#             dir(Foo).shouldnt.contain("should")

#         def test_shouldnt_overwrite_instance_attributes():
#             """do not patch already existing instance attributes with same name"""

#             class Foo(object):
#                 def __init__(self, when, shouldnt, bar):
#                     self.when = when
#                     self.shouldnt = shouldnt
#                     self.bar = bar

#             f = Foo(42, 43, "bar")

#             f.when.should.be.equal(42)
#             f.shouldnt.should.be.equal(43)
#             f.bar.should.be.equal("bar")

#             f.__dict__.should.contain("when")
#             f.__dict__.should.contain("shouldnt")
#             f.__dict__.should.contain("bar")

#             dir(f).should.contain("when")
#             dir(f).should.contain("shouldnt")
#             dir(f).should.contain("bar")
#             dir(f).shouldnt.contain("should")

#     def test_dir_conceals_sure_specific_attributes():
#         ("dir(obj) should conceal names of methods that were grafted by sure")

#         x = 123

#         expect(set(dir(x)).intersection(set(sure.POSITIVES))).to.be.empty
#         expect(set(dir(x)).intersection(set(sure.NEGATIVES))).to.be.empty


# TODO
# def test_it_works_with_non_objects():
#     ("anything that inherits from non-object should also be patched")

#     class Foo:
#         pass

#     f = Foo()

#     f.should.be.a(Foo)

# def test_can_override_properties():
#     x =1
#     x.should = 2
#     assert x.should == 2
