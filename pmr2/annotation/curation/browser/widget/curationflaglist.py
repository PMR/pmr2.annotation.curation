import zope.component
import zope.interface

from z3c.form.interfaces import IFieldWidget
from z3c.form.field import Fields

from z3c.form.object import ObjectSubForm, makeDummyObject

from z3c.form.browser.widget import HTMLFormElement
from z3c.form.browser.multi import MultiWidget
from z3c.form.browser.object import ObjectWidget
from z3c.form.widget import FieldWidget
from z3c.form.browser import widget

from pmr2.annotation.curation.browser.widget import interfaces
from pmr2.annotation.curation.interfaces import ICurationTool
from pmr2.annotation.curation.tool import buildSchemaInterface


class CurationFlagListSelectMultiWidget(MultiWidget):
    """\
    Original Multi Version.
    """
    zope.interface.implements(interfaces.ICurationFlagListSelectWidget)

    klass = u'curationflaglistselect-widget'
    items = ()

    showLabel = True # show labels for item subwidgets or not

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(CurationFlagListSelectWidget, self).update()

    def updateAllowAddRemove(self):
        # Disallow adding or removing by end-users as we provide the
        # values.
        self.allowAdding = self.allowRemoving = False


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


@zope.interface.implementer(IFieldWidget)
def BasicCurationDictFieldWidget(field, request):
    """IFieldWidget factory for BasicCurationDict."""
    # While I could get the BasicCurationDict to implement IObject,
    # doing this additional step may allow finer control later.
    return FieldWidget(field, CurationFlagListWidget(request))
