import unittest

from zope.testing import doctestunit, doctest
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

from pmr2.annotation.curation.tests import base


def test_suite():
    return unittest.TestSuite([

        doctestunit.DocTestSuite(
            module='pmr2.annotation.curation.schema.field',
            setUp=testing.setUp, tearDown=testing.tearDown
        ),

        doctestunit.DocTestSuite(
            module='pmr2.annotation.curation.converter',
            setUp=testing.setUp, tearDown=testing.tearDown
        ),

        ztc.ZopeDocFileSuite(
            'browser/form.txt', package='pmr2.annotation.curation',
            test_class=ptc.FunctionalTestCase,
            optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS,
        ),

    ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
