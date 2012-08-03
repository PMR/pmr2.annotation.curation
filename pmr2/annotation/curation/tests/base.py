from os.path import dirname, join
import tempfile
import shutil
import unittest

from zope.testing import doctestunit, doctest
from zope.component import testing

import zope.interface
import zope.component
from zope.annotation import IAnnotations
import z3c.form.testing

from Zope2.App import zcml
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup, onteardown

from pmr2.app.exposure.tests import base


@onsetup
def setup():
    import pmr2.annotation.curation
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', pmr2.annotation.curation)
    fiveconfigure.debug_mode = False
    ztc.installPackage('pmr2.annotation.curation')

@onteardown
def teardown():
    pass

setup()
teardown()
ptc.setupPloneSite(products=('pmr2.annotation.curation',))


class TestCase(ptc.PloneTestCase):
    pass


class CompleteDocTestCase(base.CompleteDocTestCase):

    def setUp(self):
        super(CompleteDocTestCase, self).setUp()

        from pmr2.app.exposure.content import Exposure, ExposureFile

        from pmr2.annotation.curation.content import MasterCurationFlag
        from pmr2.annotation.curation.content import CurationValue
        from pmr2.annotation.curation.interfaces import ICurationTool

        def curation_value(id_, title):
            value = CurationValue()
            value.id = 'c' + id_
            value.title = title
            return value

        def master_flag(id, title, values):
            flag = MasterCurationFlag()
            flag.id = id
            flag.title = title
            flag.values = [curation_value(v, unicode(v)) for v in values]
            return flag

        # Add in basic curation flags.
        curation = zope.component.getUtility(ICurationTool)
        curation.addFlag(
            master_flag('status', u'Curation Status', list('0123')))
        curation.addFlag(
            master_flag('software', u'Software Rating', list('0123')))

        # Add in the exposure file which we will test with.
        context = self.portal.exposure['1']
        file1 = ExposureFile('file1')
        context['file1'] = file1
        context['file1'].reindexObject()
