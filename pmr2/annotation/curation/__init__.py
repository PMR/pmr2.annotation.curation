import zope.i18nmessageid

from pmr2.app.annotation import note_factory as factory

from pmr2.annotation.curation.note import BasicCurationNote

BasicCurationNoteFactory = factory(BasicCurationNote, 'basic_curation')
MessageFactory = zope.i18nmessageid.MessageFactory('pmr2.oauth')
