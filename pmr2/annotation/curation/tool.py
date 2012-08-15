import new

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
from pmr2.annotation.curation.schema import SequenceChoice

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


def buildSchemaInterface(flags, name=None,
        _vocabulary='pmr2.curation.simple_curation_vocab'):
    """\
    Build a schema interface based on the flags 

    curation_set_id -
        The curation set id to use.  Default is `None` currently as
        this feature is not implemented yet.
    """

    # Dragons in this method.

    default = {
        '__module__': __name__,
        '__doc__': 'Dynamic interface',
    }

    if name is None:
        name = 'ICurationFlagSchema'

    fields = {}
    for c, f in enumerate(sorted(flags.items())):
        k, v = f
        field = SequenceChoice(
            title=v.title,
            required=False,
            # XXX placeholder: this will NOT reflect the value
            vocabulary=_vocabulary,
        )
        field.order = c
        fields[k] = field

    default.update(fields)

    # Incoming lion, get in the car.
    interfaceClass = new.classobj(name, (zope.interface.Interface,), default)

    return interfaceClass
    # actual data assignment should be done via dict datamanager.
