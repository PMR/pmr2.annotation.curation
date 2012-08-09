import zope.component
import zope.interface

from z3c.form import interfaces
from z3c.form import widget
from z3c.form import button
from z3c.form.browser.widget import HTMLFormElement
from z3c.form.browser.multi import MultiWidget

from pmr2.annotation.curation.browser.widget import interfaces


class CurationFlagListSelectWidget(MultiWidget):
    zope.interface.implements(interfaces.ICurationFlagListSelectWidget)

    klass = u'curationflaglistselect-widget'
    items = ()

    showLabel = True # show labels for item subwidgets or not

    def update(self):
        """See z3c.form.interfaces.IWidget."""
        super(CurationFlagListSelectWidget, self).update()

    def updateAllowAddRemove(self):
        # Disallow adding or removing by end-users as we provide the
        # values.
        self.allowAdding = self.allowRemoving = False
