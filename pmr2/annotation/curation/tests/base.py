from os.path import dirname, join
import tempfile
import shutil
import unittest

from zope.testing import doctestunit, doctest
from zope.component import testing

import zope.interface
import zope.component
from zope.annotation import IAnnotations
import z3c.form.testing

from Zope2.App import zcml
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup, onteardown


@onsetup
def setup():
    import pmr2.annotation.curation
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', pmr2.annotation.curation)
    fiveconfigure.debug_mode = False

@onteardown
def teardown():
    pass

setup()
teardown()
ptc.setupPloneSite(products=('pmr2.annotation.curation',))
