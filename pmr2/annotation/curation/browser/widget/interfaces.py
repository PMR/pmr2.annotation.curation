from z3c.form.interfaces import ITextAreaWidget
from z3c.form.interfaces import IMultiWidget
from z3c.form.interfaces import IObjectWidget


class ICurationDictWidget(IMultiWidget):
    """Curation Dict Widget."""


class ICurationFlagDictWidget(ITextAreaWidget):
    """Curation Flag Dict Widget."""


class ICurationFlagListWidget(IObjectWidget):
    """Curation Flag List Select Widget."""
