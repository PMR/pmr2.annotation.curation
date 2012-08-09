from unittest import TestCase, TestSuite, makeSuite

import zope.interface
import zope.component
import zope.schema

from zope.interface.verify import verifyClass

from pmr2.annotation.curation.interfaces import *
from pmr2.annotation.curation.tool import CurationToolAnnotation
from pmr2.annotation.curation.tool import buildSchemaInterface

from pmr2.annotation.curation.content import MasterCurationFlag
from pmr2.annotation.curation.content import CurationValue


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


class BuildSchemaInterfaceTestCase(TestCase):

    def setUp(self):
        def curation_value(i):
            result = CurationValue()
            result.id = i
            result.title = unicode(i)
            return result

        self.tool = CurationToolAnnotation()
        self.ids = {
            'curation': ['a1', 'a2', 'a3'],
            'quality': ['b1', 'b2', 'b3'],
            'result': ['c1', 'c2', 'c3'],
        }
        for i, v in self.ids.iteritems():
            flag = MasterCurationFlag()
            flag.id = i
            flag.values = [curation_value(vv) for vv in v]
            self.tool.addFlag(flag)

    def tearDown(self):
        pass

    def test_0000_buildSchemaInterface_base(self):
        klass = buildSchemaInterface(self.tool.all_flags)
        self.assertEqual(sorted(klass.names()), sorted(self.ids.keys()))
        self.assertTrue(isinstance(klass['curation'], zope.schema.Choice))


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(CurationToolTestCase))
    suite.addTest(makeSuite(BuildSchemaInterfaceTestCase))
    return suite

