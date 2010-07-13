import zope.interface
import zope.schema

class ICurationIdMixin(zope.interface.Interface):
    """\
    Provides a generic id field attribute for use by AddForm.
    """

    id = zope.schema.DottedName(
        title=u'Id',
        description=u'The identifier of the object, used for URI.',
        min_dots=0,
    )
