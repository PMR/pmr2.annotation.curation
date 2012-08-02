import zope.interface
import zope.schema

from pmr2.annotation.curation.schema.interfaces import IBasicCurationDict
from pmr2.annotation.curation.schema.interfaces import ICurationEntry
from pmr2.annotation.curation.schema.interfaces import ICurationEntryList
from pmr2.annotation.curation.schema.interfaces import ICurationDict
from pmr2.annotation.curation.schema.interfaces import ICurationFlagDict


class CurationEntryList(zope.schema.List):
    """\
    See ICurationEntryList.
    """

    zope.interface.implements(ICurationEntryList)

    def __init__(self, **kw):
        value_type = zope.schema.List(
            title=u'Flags',
            value_type=zope.schema.Object(
                title=u'Curation Entry',
                schema=ICurationEntry,
            )
        )
        super(CurationEntryList, self).__init__(value_type, **kw)


class BasicCurationDict(zope.schema.Dict):
    """
    The basic curation dictionary
    """

    zope.interface.implements(IBasicCurationDict)

    def __init__(self, *a, **kw):
        key_type = zope.schema.DottedName(title=u'Key')
        value_type = zope.schema.List(
            title=u'Values',
            value_type=zope.schema.DottedName(title=u'Value'),
        )

        super(BasicCurationDict, self).__init__(key_type, value_type, *a, **kw)


class CurationDict(zope.schema.Dict):
    """\
    Curation dictionary.
    """

    zope.interface.implements(
        ICurationDict, 
        zope.schema.interfaces.IFromUnicode,
    )

    def __init__(self, **kw):
        key_type = zope.schema.TextLine(
            title=u'Key',
        )
        value_type = zope.schema.List(
            title=u'Values',
            value_type=zope.schema.TextLine(title=u'Values',),
        )
        super(CurationDict, self).__init__(key_type, value_type, **kw)


    def fromUnicode(self, u):
        """\
        >>> d = CurationDict()
        >>> d.fromUnicode(u'key:value')
        {u'key': [u'value']}

        >>> result = d.fromUnicode(u'key:value\\nkey2:type2\\nkey:value2')
        >>> result[u'key']
        [u'value', u'value2']
        >>> result[u'key2']
        [u'type2']

        >>> d.fromUnicode(u'key:value\\nkey2\\nkey3:value3')
        Traceback (most recent call last):
        ...
        InvalidValue: Invalid curation string
        """

        result = {}
        for i in u.splitlines():
            lines = i.split(u':', 1)
            if len(lines) != 2:
                raise zope.schema.interfaces.InvalidValue(
                    'Invalid curation string')
            k, v = lines
            if k not in result:
                result[k] = []
            result[k].append(v)
        return result


class CurationFlagDict(zope.schema.Dict):
    """\
    Curation flag dictionary.

    The values for this are represented in unicode in two lines for each
    entry, first line being the key, second being the value.
    """

    zope.interface.implements(
        ICurationFlagDict, 
        zope.schema.interfaces.IFromUnicode,
    )

    def __init__(self, **kw):
        key_type = zope.schema.TextLine(
            title=u'Key',
            description=u'A valid value for this curation flag',
        )
        value_type = zope.schema.TextLine(
            title=u'Value',
            description=u'Definition of this value.',
        )
        super(CurationFlagDict, self).__init__(key_type, value_type, **kw)

    def fromUnicode(self, u):
        """\
        >>> d = CurationFlagDict()
        >>> d.fromUnicode(u'key\\nvalue')
        {u'key': u'value'}

        >>> r = d.fromUnicode(u'key\\nvalue\\nkey2\\ntype2\\nkey\\nvalue2')
        >>> a = {u'key': u'value2', u'key2': u'type2'}
        >>> r == a
        True

        >>> r = d.fromUnicode(u'key\\nvalue\\nkey2\\ntype2\\nkey\\n')
        >>> a = {u'key': u'', u'key2': u'type2'}
        >>> r == a
        True

        >>> r = d.fromUnicode(u'key\\nvalue\\nkey2\\ntype2\\nkey')
        >>> a = {u'key': u'', u'key2': u'type2'}
        >>> r == a
        True

        >>> r = d.fromUnicode(u'key\\n\\nkey2\\ntype2\\nkey3\\nvalue3')
        >>> a = {u'key': u'', u'key2': u'type2', u'key3': 'value3'}
        >>> r == a
        True

        >>> r = d.fromUnicode(u'key\\n\\nkey2\\ntype2\\n\\nvalue3')
        >>> a = {u'key': u'', u'key2': u'type2'}
        >>> r == a
        True

        >>> r = d.fromUnicode(u'key\\n\\n\\n\\nkey2\\ntype2')
        >>> a = {u'key': u'', u'key2': u'type2'}
        >>> r == a
        True

        """

        result = {}
        lines = u.splitlines()
        lines.reverse()
        while lines:
            key = lines.pop()
            value = lines and lines.pop() or u''
            if key:
                result[key] = value
        return result
