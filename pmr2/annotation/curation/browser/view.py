import zope.component
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from plone.z3cform import layout

from pmr2.app.exposure.browser.browser import RawContentNote
from pmr2.app.exposure.browser.browser import ExposureFileViewBase

from pmr2.annotation.curation.interfaces import ICurationTool
from pmr2.annotation.curation.browser.templates import path


class BasicCurationNote(ExposureFileViewBase):
    """\
    The basic curation note.
    """

    template = ViewPageTemplateFile(path('basic_curation_note.pt'))

    def items(self):
        curation = zope.component.getUtility(ICurationTool)
        for k, v in self.note.flags.iteritems():
            key = curation.getFlag(k)
            value = v and v[0] or '0'
            yield {
                'key': key,
                'value': value,
            }

# XXX need to get this needless boilerplate removed when pmr2.app
# rectifies this situation.
BasicCurationNoteView = layout.wrap_form(BasicCurationNote)
