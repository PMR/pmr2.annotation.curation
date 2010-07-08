from unittest import TestCase, TestSuite, makeSuite

import zope.interface
import zope.component

from zope.interface.verify import verifyClass
from zope.publisher.interfaces import IPublishTraverse
from paste.httpexceptions import HTTPNotFound, HTTPFound

from pmr2.annotation.curation.interfaces import *
from pmr2.annotation.curation.tool import CurationToolAnnotation


class MockCurationFlag:
    zope.interface.implements(ICurationFlag)
    def __init__(self, title):
        self.title = title


class CurationToolTestCase(TestCase):

    def setUp(self):
        sm = zope.component.getSiteManager()
        # registering global mock flags
        count = 6
        self._default = [1, 2]
        self.flags = {}
        self.default_flags = {}
        flagid = lambda i: 'flag%d' % i

        # all flags
        for i in xrange(count):
            self.flags[flagid(i)] = MockCurationFlag('Flag %d' % i)

        # default flags
        for i in self._default:
            self.default_flags[flagid(i)] = self.flags[flagid(i)]
            sm.registerUtility(self.flags[flagid(i)], ICurationFlag, flagid(i))

        # the tool we test
        self.tool = CurationToolAnnotation()

    def tearDown(self):
        sm = zope.component.getSiteManager()
        flagid = lambda i: 'flag%d' % i
        for i in self._default:
            sm.unregisterUtility(self.flags[flagid(i)])

    def test_001_basic(self):
        # make sure this can retrieve global flag.
        flag1 = self.tool.getFlag('flag1')
        self.assertEqual(flag1, self.flags['flag1'])
        flag2 = self.tool.getFlag('flag2')
        self.assertEqual(flag2, self.flags['flag2'])

    def test_002_no_flag(self):
        flag = self.tool.getFlag('flag')
        self.assertEqual(flag, None)

    def test_003_new_flag(self):
        self.tool.setFlag('flag3', self.flags['flag3'])
        flag = self.tool.getFlag('flag3')
        self.assertEqual(flag, self.flags['flag3'])
        # now remove it, should now return no result
        self.tool.setFlag('flag3', None)
        flag = self.tool.getFlag('flag3')
        self.assertEqual(flag, None)

    def test_004_overwrite_default(self):
        flag = MockCurationFlag('A Flag')
        # overrides global flag
        self.tool.setFlag('flag2', flag)
        result = self.tool.getFlag('flag2')
        self.assertEqual(flag, result)
        # now remove it, should restore to original flag
        self.tool.setFlag('flag2', None)
        flag2 = self.tool.getFlag('flag2')
        self.assertEqual(flag2, self.flags['flag2'])


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(CurationToolTestCase))
    return suite

