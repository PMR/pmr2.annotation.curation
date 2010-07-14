import zope.schema
import zope.interface

from pmr2.annotation.curation.schema import CurationDict, CurationFlagDict


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
        title=u'Valid Items',
        description=u'Curation values that can be assigned to this flag; '
                     'descriptions of each value can be assigned.',
    )

    def curate(context):
        """
        Curates context and assigns flag appropriate.
        """


class ICurationNote(zope.interface.Interface):
    """\
    The interface for the annotation storing the set of curation values.
    """

    values = CurationDict(
        title=u'Values',
        description=u'Flags assigned to this object.',
    )

    reason = zope.schema.Dict(
        title=u'Reasons',
        description=u'The reason why the value was set for the flag, '
                     'identified by the key.',
        key_type=zope.schema.TextLine(
            title=u'Key'
        ),
        value_type=zope.schema.TextLine(
            title=u'Value'
        ),
    )


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
        key_type=zope.schema.TextLine(
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
