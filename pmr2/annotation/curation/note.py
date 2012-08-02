import zope.interface
import zope.component
from zope.schema import fieldproperty

from z3c.form.object import registerFactoryAdapter

from pmr2.app.annotation.note import ExposureFileNoteBase
from pmr2.app.annotation.note import ExposureFileEditableNoteBase

from pmr2.annotation.curation.interfaces import *


class CurationNote(ExposureFileEditableNoteBase):
    """\
    Note for the curation.
    """

    zope.interface.implements(ICurationNote)
    values = fieldproperty.FieldProperty(ICurationNote['values'])
