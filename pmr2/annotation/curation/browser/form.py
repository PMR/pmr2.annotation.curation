import zope.interface
import zope.component
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('pmr2.annotation.curation')

from plone.z3cform import layout
import z3c.form

from pmr2.annotation.curation.schema.interfaces import *
from pmr2.annotation.curation.interfaces import ICurationFlag
from pmr2.annotation.curation.interfaces import ICurationTool
from pmr2.annotation.curation.browser.interfaces import ICurationIdMixin
from pmr2.annotation.curation.flag import CurationFlag


class CurationToolDisplayForm(z3c.form.form.DisplayForm):
    fields = z3c.form.field.Fields(ICurationTool)

    template = ViewPageTemplateFile('manage_curation.pt')

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
    label = _(u'Curation Tool Management'))


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
        return self.context.absolute_url() + '/@@manage_curation'

CurationFlagAddFormView = layout.wrap_form(CurationFlagAddForm,
    label = _(u'Add a Curation Flag'))
