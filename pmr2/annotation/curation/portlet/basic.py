from zope import schema
from zope.formlib import form
from zope.interface import implements
import zope.component
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey
from plone.memoize.view import memoize

from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName

from pmr2.app.exposure.interfaces import IExposureFile

from pmr2.annotation.curation.browser.view import BasicCurationNote
from pmr2.annotation.curation import MessageFactory as _


class IBasicCurationPortlet(IPortletDataProvider):
    """\
    Exposure Information portlet.
    """

    curator_uri = zope.schema.ASCIILine(
        title=_(u'Curator contact'),
        description=_(u'The URI where the curator can be contacted.'),
        required=False,
    )

    # XXX to faciliate easy modification...
    contact_label = zope.schema.TextLine(
        title=_(u'Contact text'),
        description=_(u'The text label for the curator contact.'),
        default=u'Report curation issue.',
        required=False,
    )


class Assignment(base.Assignment):
    implements(IBasicCurationPortlet)

    curator_uri = schema.fieldproperty.FieldProperty(
        IBasicCurationPortlet['curator_uri'])
    contact_label = schema.fieldproperty.FieldProperty(
        IBasicCurationPortlet['contact_label'])

    def __init__(self, curator_uri='', contact_label=u''):
        if curator_uri:
            self.curator_uri = curator_uri
        if contact_label:
            self.contact_label = contact_label

    @property
    def title(self):
        return _(u'Model Curation')


class Renderer(base.Renderer, BasicCurationNote):

    index = ViewPageTemplateFile('portlet_core.pt')

    def __init__(self, *a, **kw):
        base.Renderer.__init__(self, *a, **kw)
        self.title = _(u'Model Curation')

    def update(self):
        if self.available:
            BasicCurationNote.update(self)

    def render(self):
        if self.available:
            return BasicCurationNote.render(self)

    @property
    def note(self):
        return zope.component.queryAdapter(self.context, name='basic_curation')

    @property
    def available(self):
        return (IExposureFile.providedBy(self.context) 
            and self.note 
            and self.note.flags)


class AddForm(base.AddForm):
    form_fields = form.Fields(IBasicCurationPortlet)
    label = _(u'Add Basic Curation Portlet')
    description = _(u'This portlet displays curation information derived from '
        'the basic curation annotation.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IBasicCurationPortlet)
    label = _(u'Edit Basic Curation Portlet')
    description = _(u'This portlet displays curation information derived from '
        'the basic curation annotation.')
