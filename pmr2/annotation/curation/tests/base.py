import zope.interface
import zope.component

from Zope2.App import zcml
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
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


class DocTestCase(base.CompleteDocTestCase):

    def setUpCurationTool(self):
        from pmr2.annotation.curation.content import MasterCurationFlag
        from pmr2.annotation.curation.content import CurationValue
        from pmr2.annotation.curation.interfaces import ICurationTool

        def curation_value(id_, title):
            value = CurationValue()
            # just local shortcuts.
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
            master_flag('grading', u'Grading', list('0123')))
        curation.addFlag(
            master_flag('correctness', u'Correctness', list('0123')))

    def setUp(self):
        super(DocTestCase, self).setUp()

        from pmr2.app.exposure.content import Exposure, ExposureFile
        from pmr2.app.exposure.content import ExposureFileType

        # Add in the exposure file which we will test with.
        context = self.portal.exposure['1']
        file1 = ExposureFile('file1')
        context['file1'] = file1
        context['file1'].reindexObject()

        # Also create a custom exposure file type with just the curation

        self.portal['curation_type'] = ExposureFileType('curation_type')
        self.portal.curation_type.title = u'Curation Type'
        self.portal.curation_type.views = [
            u'basic_curation']
        self.portal.curation_type.tags = []
        self._publishContent(self.portal.curation_type)


class CompleteDocTestCase(DocTestCase):

    def setUp(self):
        super(CompleteDocTestCase, self).setUp()
        self.setUpCurationTool()
