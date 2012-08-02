import zope.interface
import zope.schema
from zope.schema.fieldproperty import FieldProperty

from Persistence import Persistent

from pmr2.annotation.curation.interfaces import ICurationValue
from pmr2.annotation.curation.interfaces import IMasterCurationFlag


class CurationValue(Persistent):

    zope.interface.implements(ICurationValue)

    id = FieldProperty(ICurationValue['id'])
    title = FieldProperty(ICurationValue['title'])
    description = FieldProperty(ICurationValue['description'])


class MasterCurationFlag(Persistent):

    zope.interface.implements(IMasterCurationFlag)

    id = FieldProperty(IMasterCurationFlag['id'])
    title = FieldProperty(IMasterCurationFlag['title'])
    description = FieldProperty(IMasterCurationFlag['description'])
    values = FieldProperty(IMasterCurationFlag['values'])
