import zope.component

import z3c.form.interfaces
import z3c.form.converter

import pmr2.annotation.curation.schema.interfaces


class CurationFlagDictDataConverter(z3c.form.converter.BaseDataConverter):
    """\
    Calls an accessor as a method to get the data within.
    """
    zope.component.adapts(
        pmr2.annotation.curation.schema.interfaces.ICurationFlagDict,
        z3c.form.interfaces.ITextAreaWidget
    )

    def toWidgetValue(self, value):
        """\
        >>> from pmr2.annotation.curation import schema
        >>> f = schema.CurationFlagDict()
        >>> c = CurationFlagDictDataConverter(f, None)
        >>> c.toWidgetValue(None)
        u''
        >>> c.toWidgetValue({})
        u''
        >>> c.toWidgetValue({u'key': u'value'})
        u'key\\nvalue'
        >>> c.toWidgetValue({u'key': u'value', u'key2': u'value2'})
        u'key\\nvalue\\nkey2\\nvalue2'
        >>> c.toWidgetValue({u'key': u'value', u'key2': u'value2',
        ...                  u'1key': u'2value'})
        u'1key\\n2value\\nkey\\nvalue\\nkey2\\nvalue2'
        """

        if not value:
            return u''
        items = value.items()
        items.sort()
        result = []
        for i in items:
            result.extend(i)
        return u'\n'.join(result)
