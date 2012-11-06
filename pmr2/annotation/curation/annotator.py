import zope.interface
import zope.component

from pmr2.app.factory import named_factory
from pmr2.app.annotation.interfaces import IExposureFileAnnotator
from pmr2.app.annotation.interfaces import IExposureFileEditAnnotator
from pmr2.app.annotation.interfaces import IExposureFilePostEditAnnotator
from pmr2.app.annotation.annotator import ExposureFileAnnotatorBase

from pmr2.annotation.curation.interfaces import *

from pmr2.annotation.curation.util import scrub_json_unicode_to_string


class BasicCurationAnnotator(ExposureFileAnnotatorBase):
    """\
    The basic model curation annotator.

    This extends upon the basic curation flags that were available as
    part of the exposure object in pmr2.app.exposure.
    """

    zope.interface.implements(IExposureFileAnnotator, 
                              IExposureFileEditAnnotator)

    title = u'Basic Model Curation'
    label = u'Model Curation'
    description = u'Basic curation flags assigned to this item.'
    for_interface = IBasicCurationSet

    def _annotate(self, data):
        # XXX wholesale reimplementation of core method.  Once a proper
        # filter is implemented by parent class we can avoid doing this.
        note = self.note
        try:
            for a, v in data:
                # XXX figure out how to gracefully handle schema errors
                # (such as missing values).
                if a == 'flags':
                    v = scrub_json_unicode_to_string(v)
                setattr(note, a, v)
        except TypeError:
            raise TypeError('%s.generate failed to return a list of ' \
                            'tuple(key, value)' % self.__class__)
        except ValueError:
            raise ValueError('%s.generate returned invalid values (not ' \
                             'list of tuple(key, value)' % self.__class__)


BasicCurationAnnotatorFactory = named_factory(BasicCurationAnnotator)
