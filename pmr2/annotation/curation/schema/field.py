import zope.interface
import zope.schema

from pmr2.annotation.curation.schema.interfaces import ICurationDict


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
