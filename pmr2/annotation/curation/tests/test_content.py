from unittest import TestCase, TestSuite, makeSuite

import zope.interface
import zope.component

from zope.schema.interfaces import WrongType, WrongContainedType

from pmr2.annotation.curation.interfaces import *
from pmr2.annotation.curation.tool import CurationToolAnnotation
from pmr2.annotation.curation.content import CurationValue, MasterCurationFlag


class CurationToolTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_0000_base(self):
        value1 = CurationValue()
        value1.id = 'value1'
        value1.title = u'Test Value 1'

        flag1 = MasterCurationFlag()
        flag1.id = 'flag1'
        flag1.values = [value1]

    def test_0010_invalid_value(self):
        flag1 = MasterCurationFlag()
        flag1.id = 'flag1'
        self.assertRaises(WrongType,
            setattr, flag1, 'values', object)
        self.assertRaises(WrongContainedType,
            setattr, flag1, 'values', [object])


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(CurationToolTestCase))
    return suite

