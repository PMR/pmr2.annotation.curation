import zope.interface
import zope.component

from zope.app.component.hooks import getSite
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.publisher.interfaces import IPublishTraverse
from zope.publisher.interfaces import NotFound

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('pmr2.annotation.curation')

from plone.z3cform import layout
from plone.memoize.view import memoize
import z3c.form

from Products.CMFCore.utils import getToolByName

from pmr2.app.browser import form

from pmr2.annotation.curation.schema.interfaces import *
from pmr2.annotation.curation.interfaces import ICurationFlag
from pmr2.annotation.curation.interfaces import ICurationTool
from pmr2.annotation.curation.flag import CurationFlag

from pmr2.annotation.curation.browser.templates import path

from pmr2.annotation.curation.browser.interfaces import *
from pmr2.annotation.curation.browser.layout import TraverseFormWrapper


class CurationToolDisplayForm(z3c.form.form.DisplayForm):
    fields = z3c.form.field.Fields(ICurationTool).omit(
        'custom_flags', 'inactive_flags')

    template = ViewPageTemplateFile(path('manage_curation.pt'))

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


class CurationFlagAddForm(form.AddForm):
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


class CurationFlagEditForm(z3c.form.form.EditForm):
    zope.interface.implements(ICurationFlagEditForm)
    fields = z3c.form.field.Fields(ICurationFlag)
    flag = None

    def publishTraverse(self, request, name):
        if self.flag is not None:
            # we only go down one layer.
            raise NotFound(self.context, self.context.title_or_id())
        tool = zope.component.getUtility(ICurationTool)
        self.flag = tool.getFlag(name)
        if self.flag is None:
            raise NotFound(self.context, self.context.title_or_id())
        self.flagid = name
        return self

    def getContent(self):
        return self.flag

    def update(self):
        if self.getContent() is None:
            raise NotFound(self.context, self.context.title_or_id())
        return super(CurationFlagEditForm, self).update()

    def applyChanges(self, data):
        changes = super(CurationFlagEditForm, self).applyChanges(data)
        # need to wake up tool so whatever magic that commits the 
        # changes can happen.
        if changes:
            tool = zope.component.getUtility(ICurationTool)
            tool.setFlag(self.flagid, self.getContent())
        return changes
