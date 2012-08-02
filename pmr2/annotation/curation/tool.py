from persistent import Persistent
from zope.annotation import factory, IAttributeAnnotatable
from zope.app.container.contained import Contained
from zope.app.component.hooks import getSite, getSiteManager
import zope.schema
import zope.interface
import zope.component

from pmr2.app.workspace.interfaces import IWorkspaceContainer
from pmr2.app.settings.interfaces import IPMR2GlobalSettings
from pmr2.app.settings.interfaces import IPMR2PluggableSettings
from pmr2.app.factory import NamedUtilBase

from pmr2.annotation.curation.interfaces import IMasterCurationFlag
from pmr2.annotation.curation.interfaces import ICurationFlag
from pmr2.annotation.curation.interfaces import ICurationTool

__all__ = [
    'CurationTool',
]


class CurationToolAnnotation(Persistent, Contained):
    """\
    Please refer to ICurationTool
    """

    zope.interface.implements(ICurationTool)
    zope.component.adapts(IAttributeAnnotatable)

    all_flags = zope.schema.fieldproperty.FieldProperty(
        ICurationTool['all_flags'])

    def __init__(self, *a, **kw):
        super(CurationToolAnnotation, self).__init__(*a, **kw)
        self.all_flags = {}

    def getFlag(self, name):
        return self.all_flags.get(name, None)

    def addFlag(self, flag):
        if not IMasterCurationFlag.providedBy(flag):
            raise ValueError('value must be a valid master curation flag.')

        if self.getFlag(flag.id):
            raise ValueError('flag `%s` already exists.' % flag.id)

        self.all_flags[flag.id] = flag

    def delFlag(self, name):
        if self.getFlag(name):
            self.all_flags.pop(name)

    def keys(self):
        return sorted(self.all_flags.keys())

CurationTool = factory(CurationToolAnnotation)
