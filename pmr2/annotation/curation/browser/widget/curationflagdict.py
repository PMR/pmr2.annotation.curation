import zope.component
import zope.interface
import zope.schema
import zope.schema.interfaces
from zope.i18n import translate

from z3c.form import interfaces
from z3c.form.widget import FieldWidget
from z3c.form.browser.textarea import TextAreaWidget

from pmr2.annotation.curation.browser.widget import interfaces


class CurationFlagDictWidget(TextAreaWidget):
    """Ordered-Select widget implementation."""
    zope.interface.implementsOnly(interfaces.ICurationFlagDictWidget)

    cols = 60
    rows = 15


def CurationFlagDictWidgetFactory(field, request):
    return FieldWidget(field, CurationFlagDictWidget(request))

