import zope.component
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

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
        # Flags could be None...
        flags = self.note.flags or {}
        for k, v in flags.iteritems():
            key = curation.getFlag(k)

            # XXX this can be None, workaround
            if key is None:
                key = type('DummyFlag', (object,), {'title': k})

            if v:
                value = v[0]
                yield {
                    'key': key,
                    'value': value,
                }
