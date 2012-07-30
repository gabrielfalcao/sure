#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback
from datetime import datetime
from os.path import dirname, abspath, join
from misaka import (
    BaseRenderer,
    Markdown,
    EXT_FENCED_CODE,
    EXT_NO_INTRA_EMPHASIS,
)

BASE_PATH = abspath(join(dirname(__file__), '..'))


class READMETestRunner(BaseRenderer):
    test_base_path = BASE_PATH
    tests = [{}]

    def block_code(self, code, language):
        if language != 'python':
            return

        item = self.tests[-1]
        item[u'code'] = unicode(code)
        if 'title' not in item:
            item[u'title'] = u'Test #{0}'.format(len(self.tests))
            self.tests.append({})

    def header(self, title, level):
        self.tests.append({
            u'title': unicode(title),
        })

    def postprocess(self, full_document):
        actual_tests = [t for t in self.tests if 'code' in t]
        for test in actual_tests:
            sys.stdout.write("{0} ...".format(test['title']))
            before = datetime.now()
            failure = None
            lines = test['code'].splitlines()
            try:
                code = compile(test['code'], "README.md", "exec")
                eval(code)
            except Exception:
                failure = sys.exc_info()

            after = datetime.now()

            shift = before - after
            ms = shift.microseconds / 1000
            if not failure:
                print "OK ({0}ms)".format(ms)
            else:
                print "Failed ({0}ms)".format(ms)
                exc, name, tb = failure
                tb = tb.tb_next
                line = lines[tb.tb_lineno - 1]
                print "Traceback (most recent call last):"
                print "{0}     {1}".format(traceback.format_tb(tb)[-1], line)
                # print u'  File README.md, line {0}'.format(tb.next)


renderer = READMETestRunner()

md = Markdown(
    renderer,
    extensions=EXT_FENCED_CODE | EXT_NO_INTRA_EMPHASIS,
)

text = open(join(BASE_PATH, 'README.md')).read()
md.render(text)
