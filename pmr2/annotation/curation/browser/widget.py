import zope.component
import zope.interface

import z3c.form.interfaces
from z3c.form.browser import textarea
from z3c.form.widget import FieldWidget


class CurationFlagDictWidget(textarea.TextAreaWidget):
    """Basic curation flag widget"""
    cols = 60
    rows = 15

@zope.component.adapter(zope.schema.interfaces.IField,
        z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def CurationFlagDictWidgetFactory(field, request):
    return FieldWidget(field, CurationFlagDictWidget(request))

