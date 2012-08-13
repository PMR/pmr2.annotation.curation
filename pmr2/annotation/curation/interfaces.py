import zope.schema
import zope.interface

from pmr2.annotation.curation.schema import BasicCurationDict
from pmr2.annotation.curation.schema import CurationFlagDict


# Interfaces

class ICurationLayer(zope.interface.Interface):
    """\
    Marker interface for this product.
    """


class ICurationValue(zope.interface.Interface):
    """\
    Interface for the base curation value.
    """

    id = zope.schema.DottedName(
        title=u'Id',
        description=u'Identifier for this attribute',
        required=True,
    )

    title = zope.schema.TextLine(
        title=u'Title',
        description=u'Short description for this value',
        required=True,
    )

    description = zope.schema.Text(
        title=u'Description',
        description=u'Long description for this value',
        required=False,
    )


class IMasterCurationFlag(zope.interface.Interface):
    """\
    Interface for the master curation flag.

    This is the master flag, it contains the valid values that can be
    assigned to curation sets that make use of this.
    """

    id = zope.schema.DottedName(
        title=u'Id',
        description=u'Identifier for this master curation flag',
        required=True,
    )

    title = zope.schema.TextLine(
        title=u'Title',
        description=u'Short description for this value',
        required=True,
    )

    description = zope.schema.Text(
        title=u'Description',
        description=u'Long description for this value',
        required=False,
    )

    values = zope.schema.List(
        title=u'Valid flags',
        description=u'The list of valid curation values that can be '
                     'assigned to this flag.',
        value_type=zope.schema.Object(schema=ICurationValue),
    )


class IMasterCurationFlagSet(zope.interface.Interface):
    """
    A set of master curation flags.
    """

    id = zope.schema.DottedName(
        title=u'Id',
        description=u'Identifier for this set of master curation flag',
        required=True,
    )

    title = zope.schema.TextLine(
        title=u'Title',
        required=True,
    )

    description = zope.schema.Text(
        title=u'Description',
        required=False,
    )

    values = zope.schema.Set(
        title=u'Flag IDs',
        description=u'A set of flags from the master set of master curation '
                     'flags that belong to this set.',
        value_type=zope.schema.DottedName()
    )


class IBasicCurationSet(zope.interface.Interface):
    """\
    Set of curation assigned.

    A dictionary containing curation assigned to this context.

    The keys are the ids of a defined MasterCurationFlag, and values are
    the ids of the curation value it contains.
    """

    flags = BasicCurationDict(
        title=u'Curation Flags',
        description=u'Curation flags assigned to this object.',
    )


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


class ICurationTool(zope.interface.Interface):
    """\
    The interface to the curation tool.  
    
    The class implementing this interface will be a utility registered 
    to the site and stored as one of its annotations.  The attributes
    here are custom flags available for selection by end users via the
    curation assignment widget and/or web-services.
    """

    all_flags = zope.schema.Dict(
        title=u'All Flags',
        description=u'All curation flags available for use in curation.',
        key_type=zope.schema.DottedName(),
        value_type=zope.schema.Object(schema=IMasterCurationFlag),
        default=None,
    )

    def getFlag(name):
        """\
        Get a curation flag.

        name - the identifier for the flag.
        """

    def setFlag(name, flag):
        """\
        Sets a custom curation flag using the name.

        name - the identifier for the flag.
        """

    def delFlag(name):
        """\
        Deletes a custom curation flag using the name.

        name - the identifier for the flag.
        """

    def keys():
        """\
        Returns a list of keys for all flags.
        """
