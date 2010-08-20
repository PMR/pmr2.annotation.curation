import zope.schema
import zope.interface

from pmr2.annotation.curation.schema.interfaces import ICurationEntry

from pmr2.annotation.curation.schema import CurationDict
from pmr2.annotation.curation.schema import CurationEntryList
from pmr2.annotation.curation.schema import CurationFlagDict


# Interfaces

class ICurationLayer(zope.interface.Interface):
    """\
    Marker interface for this product.
    """


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

    items = CurationFlagDict(
        title=u'Valid Flag Values',
        description=u'Curation values that can be assigned to this flag; '
                     'descriptions of each value can be assigned.',
    )

    def curate(context):
        """
        Curates context and assigns flag appropriate.
        """


class ICurationEntry(zope.interface.Interface):
    """\
    A curation flag entry for the curation note
    """

    id = zope.schema.TextLine(
        title=u'Id',
        description=u'The identifier of the curation flag.',
    )

    selected = zope.schema.List(
        title=u'Selected',
        description=u'Values of this curation flag assigned to the object.',
        #vocabulary=This is going to be fun...,
        value_type=zope.schema.TextLine(title=u'Values',),
    )

    #values = zope.schema.List(
    #    title=u'Values',
    #    description=u'Values of this curation flag assigned to the object.',
    #    #vocabulary=This is going to be fun...,
    #    value_type=zope.schema.TextLine(title=u'Values',),
    #)



class ICurationNote(zope.interface.Interface):
    """\
    The interface for the annotation storing the set of curation values.
    """

    # TODO in the future we may need a vocabulary to store subsets of 
    # applicable curation flag for the item this note is attached to.

    values = zope.schema.List(
        title=u'Values',
        description=u'Flags assigned to this object.',
        value_type=zope.schema.Object(
            title=u'Curation Entry',
            schema=ICurationEntry,
        )
    )

    #values = CurationEntryList(
    #    title=u'Values',
    #    description=u'Flags assigned to this object.',
    #)

    #reason = zope.schema.Dict(
    #    title=u'Reasons',
    #    description=u'The reason why the value was set for the flag, '
    #                 'identified by the key.',
    #    key_type=zope.schema.TextLine(
    #        title=u'Key'
    #    ),
    #    value_type=zope.schema.TextLine(
    #        title=u'Value'
    #    ),
    #)


class ICurationTool(zope.interface.Interface):
    """\
    The Curation tool.  Will be a utility that is registered, has an
    annotation component where custom flags can be stored.  Provides
    methods to access curation flags.  Provide a way to store flags.
    """

    custom_flags = zope.schema.Dict(
        title=u'Custom Flags',
        description=u'Custom flags defined for this tool',
        default={},
        key_type=zope.schema.DottedName(
            title=u'Key',
        ),
        # value_type should be things that implement ICurationFlag.
    )

    inactive_flags = zope.schema.List(
        title=u'Inactive Flags',
        description=u'Flags not available for usage.',
        required=False,
        default=[],
    )

    def getFlag(name):
        """\
        Returns the curation flag with the given name.
        """

    def isActive(name):
        """\
        Tests whether the flag with the given name is active.
        """

    def listActiveFlags():
        """\
        Returns a list of flags active flags that are available for use.
        """

    def listFlags():
        """\
        Returns a list of all available flags.
        """

    def setFlag(name, flag):
        """\
        Sets a custom curation flag using the name.

        None value removes it.
        """
