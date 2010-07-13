import zope.schema.interfaces


class CurationFlagExistError(zope.schema.interfaces.ValidationError):
    """\
    Curation flag already exists.
    """


class ICurationDict(zope.schema.interfaces.IDict):
    """\
    Curation dictionary.
    """
