import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
ptc.setupPloneSite()

import d3kod.restapi
from d3kod.restapi import testing as d3kodtesting

optionflags = (doctest.NORMALIZE_WHITESPACE|
                doctest.ELLIPSIS|
                doctest.REPORT_NDIFF)



class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            ztc.installPackage(d3kod.restapi)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    suite = unittest.TestSuite([

        # Unit tests
        doctestunit.DocFileSuite(
            'tests/restapi.txt', package='d3kod.restapi',
            setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='d3kod.restapi.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='d3kod.restapi',
        #    test_class=TestCase),

        ztc.FunctionalDocFileSuite(
            'tests/browser.txt', package='d3kod.restapi',
            optionflags=optionflags,
            test_class=ptc.FunctionalTestCase),

        ])
    suite.layer = d3kodtesting.layer
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
