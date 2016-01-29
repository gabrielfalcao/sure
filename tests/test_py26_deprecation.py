# -*- coding: utf-8 -*-

import warnings

from mock import patch


def test_deprecation_warning_py26():
    """test deprecation warning in python 2.6"""
    with patch("sys.version_info") as version_info_patch, warnings.catch_warnings(record=True) as captured_warnings:
        from sure import print_py26_deprecation_warn

        # do not expect deprecation warning if python 2.7
        version_info_patch.major = 2
        version_info_patch.minor = 7
        print_py26_deprecation_warn()
        captured_warnings.should.be.empty

        # expect deprecation warning if python 2.6
        version_info_patch.major = 2
        version_info_patch.minor = 6
        print_py26_deprecation_warn()

        captured_warnings.should.have.length_of(1)
        captured_warnings[0].category.should.be.equal(PendingDeprecationWarning)
        str(captured_warnings[0].message).should.be.equal("The next version of sure will NO LONGER support python 2.6")
