# -*- coding: utf-8 -*-

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
