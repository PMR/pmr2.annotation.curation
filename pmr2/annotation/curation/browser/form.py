import zope.interface
import zope.component
from zope.app.component.hooks import getSite
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('pmr2.annotation.curation')
from zope.publisher.interfaces import IPublishTraverse
from plone.z3cform import layout
from plone.memoize.view import memoize
import z3c.form
from paste.httpexceptions import HTTPNotFound, HTTPFound
from Products.CMFCore.utils import getToolByName

from pmr2.annotation.curation.schema.interfaces import *
from pmr2.annotation.curation.interfaces import ICurationFlag
from pmr2.annotation.curation.interfaces import ICurationTool
from pmr2.annotation.curation.flag import CurationFlag

from pmr2.annotation.curation.browser.interfaces import *
from pmr2.annotation.curation.browser.layout import TraverseFormWrapper


class CurationToolDisplayForm(z3c.form.form.DisplayForm):
    fields = z3c.form.field.Fields(ICurationTool)

    template = ViewPageTemplateFile('manage_curation.pt')

    def portal_url(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        return portal.absolute_url()

    def getContent(self):
        return zope.component.getUtility(ICurationTool)

    def flags(self):
        tool = self.getContent()
        flags = tool.listFlags()
        keys = ['id', 'flag']
        return [dict(zip(keys, flag)) for flag in flags.items()]

    def __call__(self):
        return self.render()

CurationToolDisplayFormView = layout.wrap_form(CurationToolDisplayForm,
    label=_(u'Curation Tool Management'))


class CurationFlagAddForm(z3c.form.form.AddForm):
    fields = z3c.form.field.Fields(ICurationIdMixin) + \
             z3c.form.field.Fields(ICurationFlag).omit('items')

    def create(self, data):
        self.data = data
        flag = CurationFlag()
        flag.title = data['title']
        flag.description = data['description']
        return flag

    def add(self, obj):
        tool = zope.component.getUtility(ICurationTool)
        name = self.data['id']
        if tool.getFlag(name):
            # Currently we don't support overriding builtin flags.
            raise CurationFlagExistsError()
        tool.setFlag(name, obj)

    def nextURL(self):
        # assume context is portal root
        return '%s/@@manage-edit-curation-flag/%s' % (
            self.context.absolute_url(),
            self.data['id']
        )

CurationFlagAddFormView = layout.wrap_form(CurationFlagAddForm,
    label = _(u'Add a Curation Flag'))


class CurationFlagEditForm(z3c.form.form.EditForm):
    zope.interface.implements(ICurationFlagEditForm)
    fields = z3c.form.field.Fields(ICurationFlag)
    flag = None

    def publishTraverse(self, request, name):
        if self.flag is not None:
            # we only go down one layer.
            raise HTTPNotFound()
        tool = zope.component.getUtility(ICurationTool)
        self.flag = tool.getFlag(name)
        if self.flag is None:
            raise HTTPNotFound()
        self.flagid = name
        return self

    def getContent(self):
        return self.flag

    def update(self):
        if self.getContent() is None:
            raise HTTPNotFound()
        return super(CurationFlagEditForm, self).update()

    def applyChanges(self, data):
        changes = super(CurationFlagEditForm, self).applyChanges(data)
        # need to wake up tool so whatever magic that commits the 
        # changes can happen.
        if changes:
            tool = zope.component.getUtility(ICurationTool)
            tool.setFlag(self.flagid, self.getContent())
        return changes


CurationFlagEditFormView = layout.wrap_form(CurationFlagEditForm,
    __wrapper_class=TraverseFormWrapper,
    label = _(u'Edit Curation Flag'))

