import zope.component
import zope.interface

from z3c.form import interfaces
from z3c.form import widget
from z3c.form import button
from z3c.form.browser.widget import HTMLFormElement
from z3c.form.browser.multi import MultiWidget

from pmr2.annotation.curation.browser.widget import interfaces


class CurationFlagListSelectWidget(HTMLFormElement, widget.MultiWidget):
    zope.interface.implements(interfaces.ICurationFlagListSelectWidget)

    # based directly on the default widget

    def update(self):
        super(CurationFlagListSelectWidget, self).update()
