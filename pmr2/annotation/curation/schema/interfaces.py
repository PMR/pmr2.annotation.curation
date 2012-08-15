import zope.interface
import zope.schema.interfaces


class CurationFlagExistError(zope.schema.interfaces.ValidationError):
    """\
    Curation flag already exists.
    """


class IBasicCurationDict(zope.schema.interfaces.IDict):
    """\
    The basic curation dictionary.
    """


class ICurationDict(zope.schema.interfaces.IDict):
    """\
    Curation dictionary.
    """


class ICurationFlagDict(zope.schema.interfaces.IDict):
    """\
    Curation flag dictionary.
    """


class ISequenceChoice(zope.schema.interfaces.IChoice):
    """\
    Customized Choice that lets me discriminate my own z3c things.
    """
