import zope.component

from z3c.form.converter import BaseDataConverter
from z3c.form.converter import CollectionSequenceDataConverter
from z3c.form.interfaces import ISequenceWidget, ITextAreaWidget

from z3c.form.widget import SequenceWidget

from pmr2.annotation.curation.schema import interfaces


class CurationFlagDictDataConverter(BaseDataConverter):
    """\
    Calls an accessor as a method to get the data within.
    """
    zope.component.adapts(interfaces.ICurationFlagDict, ITextAreaWidget)

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


class SequenceChoiceDataConverter(CollectionSequenceDataConverter):
    """\
    Apply the intended conversion class to the choice widget.
    """

    zope.component.adapts(interfaces.ISequenceChoice, ISequenceWidget)

    def toFieldValue(self, value):
        """\
        Modified from parent to handle the noValueToken.

        >>> from pmr2.testing.base import TestRequest
        >>> from z3c.form import term
        >>> from z3c.form.browser.select import SelectWidget
        >>> from pmr2.annotation.curation import schema
        >>> from pmr2.annotation.curation import vocab
        >>> curation_values = vocab.SimpleCurationValueVocab(None)
        >>> terms = term.Terms()
        >>> terms.terms = curation_values
        >>> widget = SelectWidget(TestRequest())
        >>> field = schema.SequenceChoice(values=['c1', 'c2', 'c3'])
        >>> widget.field = field
        >>> widget.terms = terms
        >>> c = SequenceChoiceDataConverter(field, widget)
        >>> c.toFieldValue([])
        []
        >>> c.toFieldValue(['c1'])
        ['c1']
        >>> c.toFieldValue(['--NOVALUE--'])
        []
        """

        widget = self.widget
        if widget.terms is None:
            widget.updateTerms()
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]
        return collectionType([widget.terms.getValue(token) 
            for token in value if token != SequenceWidget.noValueToken])
