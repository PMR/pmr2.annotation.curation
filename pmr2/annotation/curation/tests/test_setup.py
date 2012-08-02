from unittest import TestSuite, makeSuite

import zope.component
from zope.schema.interfaces import IVocabularyFactory

from pmr2.annotation.curation.interfaces import ICurationTool
from pmr2.annotation.curation.tests.base import TestCase


class TestProductInstall(TestCase):

    def test_0000_toolInstalled(self):
        u = zope.component.getUtility(ICurationTool)
        self.assertTrue(ICurationTool.providedBy(u))
        self.assertEqual(u.keys(), [])


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite
