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
        self.flag1 = MockCurationFlag('Flag 1')
        self.flag2 = MockCurationFlag('Flag 2')
        sm.registerUtility(self.flag1, ICurationFlag, 'flag1')
        sm.registerUtility(self.flag2, ICurationFlag, 'flag2')
        self.tool = CurationToolAnnotation()

    def tearDown(self):
        sm = zope.component.getSiteManager()
        sm.unregisterUtility(self.flag1)
        sm.unregisterUtility(self.flag2)

    def test_001_basic(self):
        # make sure this can retrieve global flag.
        flag1 = self.tool.getFlag('flag1')
        self.assertEqual(flag1, self.flag1)
        flag2 = self.tool.getFlag('flag2')
        self.assertEqual(flag2, self.flag2)

    def test_002_no_flag(self):
        flag = self.tool.getFlag('flag')
        self.assertEqual(flag, None)

    def test_003_new_flag(self):
        flag3 = MockCurationFlag('Flag 3')
        self.tool.setFlag('flag3', flag3)
        flag = self.tool.getFlag('flag3')
        self.assertEqual(flag, flag3)
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
        self.assertEqual(flag2, self.flag2)


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(CurationToolTestCase))
    return suite

