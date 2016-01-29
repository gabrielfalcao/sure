# -*- coding: utf-8 -*-

from sure import expect
import sys
import warnings

from mock import patch


def test_deprecation_warning_py26():
    """test deprecation warning in python 2.6"""
    with patch.object(sys, "version_info") as version_info_patch, warnings.catch_warnings(record=True) as captured_warnings:
        from sure import print_py26_deprecation_warn

        # do not expect deprecation warning if python 2.7
        version_info_patch.__getitem__.side_effect = [2, 7]
        print_py26_deprecation_warn()
        expect(captured_warnings).should.be.empty

        version_info_patch.__getitem__.side_effect = [2, 6]
        print_py26_deprecation_warn()

        expect(captured_warnings).should.have.length_of(1)
        expect(captured_warnings[0].category).should.be.equal(PendingDeprecationWarning)
        expect(str(captured_warnings[0].message)).should.be.equal("The next version of sure will NO LONGER support python 2.6")
