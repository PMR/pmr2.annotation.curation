import zope.interface
import zope.component
from zope.schema import fieldproperty

from pmr2.app.annotation.note import ExposureFileNoteBase
from pmr2.app.annotation.note import ExposureFileEditableNoteBase

from pmr2.annotation.curation.interfaces import ICurationFlag


class CurationFlag(object):
    """\
    Basic curation flag.
    """

    zope.interface.implements(ICurationFlag)
    title = fieldproperty.FieldProperty(ICurationFlag['title'])
    description = fieldproperty.FieldProperty(ICurationFlag['description'])
    items = fieldproperty.FieldProperty(ICurationFlag['items'])
