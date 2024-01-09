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


"""
Test fix of bug described in GitHub Issue #19.
"""

import base64

from sure import expect


def test_issue_136():
    "Test for unicode error when comparing bytes"
    data_b64 = (
        'MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQg11zwkcKSsSppm8Du13'
        'je6lmwR7hEVeKMw5L8NQEN/CehRANCAAT9RzcGN/S9yN7mWP+xfLGEuw/TyHRBiW4c'
        'GE6AczRgske/P8eq8trs8unSJPCp0YPKrmCEcuotL/8BHQ4Y1AVK'
    )

    data = base64.b64decode(data_b64)
    expect(data).should.be.equal(data)
