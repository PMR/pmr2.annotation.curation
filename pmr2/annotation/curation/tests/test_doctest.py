import unittest
import doctest

from zope.component import testing
from Testing import ZopeTestCase as ztc

from pmr2.annotation.curation.tests import base


def test_suite():
    return unittest.TestSuite([

        doctest.DocTestSuite(
            module='pmr2.annotation.curation.schema.field',
            setUp=testing.setUp, tearDown=testing.tearDown
        ),

        doctest.DocTestSuite(
            module='pmr2.annotation.curation.converter',
            setUp=testing.setUp, tearDown=testing.tearDown
        ),

        ztc.ZopeDocFileSuite(
            'browser/view.txt', package='pmr2.annotation.curation',
            test_class=base.CompleteDocTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

        ztc.ZopeDocFileSuite(
            'browser/form.txt', package='pmr2.annotation.curation',
            test_class=base.CompleteDocTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

        ztc.ZopeDocFileSuite(
            'browser/widget/curationflaglist.txt', 
            package='pmr2.annotation.curation',
            test_class=base.DocTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
