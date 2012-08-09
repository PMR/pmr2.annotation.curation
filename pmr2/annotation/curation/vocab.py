import zope.interface
import zope.component

from zope.schema.interfaces import IVocabulary, IVocabularyFactory, ISource
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from pmr2.app.factory import vocab_factory


class SimpleCurationValueVocab(SimpleVocabulary):
    """\
    Simple placeholder vocabulary to loosen up coupling of too many
    concepts.
    """

    def __init__(self, context):
        self.context = context
        values = (
            ('c0', u'0 star'),
            ('c1', u'1 star'),
            ('c2', u'2 star'),
            ('c3', u'3 star'),
        )
        terms = [SimpleTerm(i, title=j) for i, j in values]
        super(SimpleCurationValueVocab, self).__init__(terms)

SimpleCurationValueVocabFactory = vocab_factory(SimpleCurationValueVocab)
