from plone.app.portlets.storage import PortletAssignmentMapping
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from Products.CMFCore.utils import getToolByName
from zope.component import getAdapter, getUtility, getMultiAdapter

from pmr2.annotation.curation.interfaces import IBasicCurationSet
from pmr2.annotation.curation.tests.base import TestCase, CompleteDocTestCase
from pmr2.annotation.curation.portlet import basic


class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def testPortletTypeRegistered(self):
        portlet = getUtility(IPortletType, name='pmr2.portlets.basic_curation')
        self.assertEquals(portlet.addview, 'pmr2.portlets.basic_curation')

    def testInterfaces(self):
        portlet = basic.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(IPortletType, name='pmr2.portlets.basic_curation')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)
        addview.createAndAdd(data={})
        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], basic.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        mapping['foo'] = basic.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, basic.EditForm))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn', 
            context=self.portal)
        assignment = basic.Assignment()

        renderer = getMultiAdapter((context, request, view, manager, 
            assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, basic.Renderer))


class TestRenderer(CompleteDocTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def renderer(self, context=None, request=None, view=None, manager=None, 
            assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager, 
            name='plone.rightcolumn', context=self.portal)
        assignment = assignment or basic.Assignment()

        return getMultiAdapter((context, request, view, manager, assignment),
            IPortletRenderer)

    def test_0000_render_wrong_context(self):
        r = self.renderer(context=self.portal, assignment=basic.Assignment())
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.assertTrue(output is None)

    def test_0100_render_exposure_note_missing(self):
        context = self.portal.exposure['1'].file1
        r = self.renderer(context=context, assignment=basic.Assignment())
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.assertTrue(output is None)

    def test_0110_render_exposure_note(self):
        context = self.portal.exposure['1'].file1
        note = getAdapter(context, name='basic_curation')
        note.flags = {'status': ['c2'], 'grading': ['c1'], 'correctness': []}
        r = self.renderer(context=context, assignment=basic.Assignment())
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.assertTrue(output is not None)
        self.assertTrue('Curation Status' in output)
        self.assertTrue('Grading' in output)
        self.assertTrue('Correctness' in output)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite
