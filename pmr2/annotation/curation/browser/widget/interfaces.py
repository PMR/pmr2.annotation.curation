from z3c.form.interfaces import ITextAreaWidget
from z3c.form.interfaces import IMultiWidget


class ICurationDictWidget(IMultiWidget):
    """Curation Dict Widget."""


class ICurationFlagDictWidget(ITextAreaWidget):
    """Curation Flag Dict Widget."""


class ICurationFlagListSelectWidget(IMultiWidget):
    """Curation Flag List Select Widget."""
