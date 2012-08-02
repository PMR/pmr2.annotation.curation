import zope.interface
import zope.component

from pmr2.app.factory import named_factory
from pmr2.app.annotation.interfaces import IExposureFileAnnotator
from pmr2.app.annotation.interfaces import IExposureFileEditAnnotator
from pmr2.app.annotation.interfaces import IExposureFilePostEditAnnotator
from pmr2.app.annotation.annotator import ExposureFileAnnotatorBase

from pmr2.annotation.curation.interfaces import *


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

BasicCurationAnnotatorFactory = named_factory(BasicCurationAnnotator)
