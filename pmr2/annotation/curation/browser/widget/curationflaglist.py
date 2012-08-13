import zope.component
import zope.interface

from zope.pagetemplate.interfaces import IPageTemplate

from z3c.form.interfaces import IFormLayer, IFieldWidget, ISubformFactory
from z3c.form.field import Fields

from z3c.form.object import ObjectSubForm, makeDummyObject, SubformAdapter

from z3c.form.browser.widget import HTMLFormElement
from z3c.form.browser.multi import MultiWidget
from z3c.form.browser.object import ObjectWidget
from z3c.form.widget import Widget, FieldWidget
from z3c.form.browser import widget

from pmr2.annotation.curation.browser.widget import interfaces
from pmr2.annotation.curation.interfaces import ICurationTool
from pmr2.annotation.curation.tool import buildSchemaInterface


# Object based widget and support classes.

class CurationFlagListSubForm(ObjectSubForm):

    def setupFields(self):
        # should provide method or something
        ct = zope.component.getUtility(ICurationTool)
        schema = buildSchemaInterface(ct.all_flags)
        self.fields = Fields(schema)


class CurationFlagListWidget(ObjectWidget):
    zope.interface.implements(interfaces.ICurationFlagListWidget)

    def _getForm(self, content):
        form = getattr(self, 'form', None)

        ct = zope.component.getUtility(ICurationTool)
        schema = buildSchemaInterface(ct.all_flags)

        self.subform = zope.component.getMultiAdapter(
            (content, self.request, self.context,
             form, self, self.field, makeDummyObject(schema)),
            ISubformFactory)()

    def render(self):
        """See z3c.form.interfaces.IWidget."""
        template = self.template

        ct = zope.component.getUtility(ICurationTool)
        schema = buildSchemaInterface(ct.all_flags)

        if template is None:
            template = zope.component.queryMultiAdapter(
                (self.context, self.request, self.form, self.field, self,
                 makeDummyObject(schema)),
                IPageTemplate, name=self.mode)
            if template is None:
                #return super(ObjectWidget, self).render()
                return Widget.render(self)
        return template(self)


class CurationFlagListSubformAdapter(SubformAdapter):
    """Most basic-default subform factory adapter"""

    zope.component.adapts(zope.interface.Interface, #widget value
                          IFormLayer,    #request
                          zope.interface.Interface, #widget context
                          zope.interface.Interface, #form
                          interfaces.ICurationFlagListWidget, #widget
                          zope.interface.Interface, #field
                          zope.interface.Interface) #field.schema

    factory = CurationFlagListSubForm


@zope.interface.implementer(IFieldWidget)
def BasicCurationDictFieldWidget(field, request):
    """IFieldWidget factory for BasicCurationDict."""
    # While I could get the BasicCurationDict to implement IObject,
    # doing this additional step may allow finer control later.
    return FieldWidget(field, CurationFlagListWidget(request))
