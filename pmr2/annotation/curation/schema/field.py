import zope.interface
import zope.schema

from pmr2.annotation.curation.schema.interfaces import ICurationDict
from pmr2.annotation.curation.schema.interfaces import ICurationFlagDict


class CurationDict(zope.schema.Dict):
    """\
    Curation dictionary.
    """

    zope.interface.implements(
        ICurationDict, 
        zope.schema.interfaces.IFromUnicode,
    )

    key_type = zope.schema.TextLine(
        title=u'Key',
    )
    value_type = zope.schema.List(
        title=u'Value',
        value_type=zope.schema.TextLine(title=u'Values',),
    )

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
        """

        result = {}
        for i in u.splitlines():
            k, v = i.split(u':', 1)
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

    key_type = zope.schema.TextLine(
        title=u'Key',
        description=u'A valid value for this curation flag',
    )
    value_type = zope.schema.TextLine(
        title=u'Value',
        description=u'Definition of this value.',
    )

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
        """

        result = {}
        lines = u.splitlines()
        lines.reverse()
        while lines:
            key = lines.pop()
            value = lines and lines.pop() or u''
            result[key] = value
        return result
