import zope.schema
import zope.interface

from pmr2.annotation.curation.schema import CurationDict


class ICurationFlag(zope.interface.Interface):
    """\
    Definition of a curation flag.
    """

    title = zope.schema.TextLine(
        title=u'Title',
        description=u'Short, descriptive title for this curation flag',
    )

    description = zope.schema.Text(
        title=u'Description',
    )

    items = zope.schema.Dict(
        title=u'Valid Items',
        # XXX should this be limited length/character set?
        key_type=zope.schema.TextLine(
            title=u'Key'
        ),
        value_type=zope.schema.TextLine(
            title=u'Value'
            description=u'Describes what this value is',
        ),
        description=u'Curation values that can be assigned to this flag; '
                     'descriptions of each value can be assigned.',
    )

    def curate(context):
        """
        Curates context and assigns flag appropriate.
        """


class ICuration(zope.interface.Interface):
    """\
    The interface for the annotation storing the set of curation values.
    """

    values = CurationDict(
        title=u'Values',
        description=u'Flags assigned to this object.',
    )
