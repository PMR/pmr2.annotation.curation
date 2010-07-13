import zope.interface
import zope.component

from plone.z3cform import layout
import z3c.form

from pmr2.annotation.curation.interfaces import ICurationFlag
from pmr2.annotation.curation.interfaces import ICurationTool
from pmr2.annotation.curation.browser.interfaces import ICurationIdMixin
from pmr2.annotation.curation.flag import CurationFlag


class CurationFlagAddForm(z3c.form.form.AddForm):
    fields = z3c.form.field.Fields(ICurationFlag).omit('items') + \
             z3c.form.field.Fields(ICurationIdMixin)

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
            # XXX currently we don't support overwriting builtin flags.
            # XXX not implemented exception
            raise CurationFlagExistsError()
        tool.setFlag(name, obj)

    def nextURL(self):
        pass
