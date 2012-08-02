from unittest import TestCase, TestSuite, makeSuite

import zope.interface
import zope.component

from zope.interface.verify import verifyClass

from pmr2.annotation.curation.interfaces import *
from pmr2.annotation.curation.tool import CurationToolAnnotation
from pmr2.annotation.curation.content import MasterCurationFlag


class CurationToolTestCase(TestCase):

    def setUp(self):
        self.tool = CurationToolAnnotation()

    def tearDown(self):
        pass

    def test_0000_base(self):
        self.assertEqual(self.tool.getFlag('test'), None)

    def test_0010_add_and_get(self):
        flag = MasterCurationFlag()
        flag.id = 'test'
        self.tool.addFlag(flag)
        self.assertEqual(self.tool.getFlag('test'), flag)

    def test_0020_keys(self):
        ids = ['test1', 'test2', 'test4']
        for i in ids:
            flag = MasterCurationFlag()
            flag.id = i
            self.tool.addFlag(flag)

        self.assertEqual(self.tool.keys(), ids)

    def test_0030_del(self):
        ids = ['test1', 'test2', 'test4']
        for i in ids:
            flag = MasterCurationFlag()
            flag.id = i
            self.tool.addFlag(flag)

        self.tool.delFlag('test2')
        self.assertEqual(self.tool.keys(), ['test1', 'test4'])


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(CurationToolTestCase))
    return suite

