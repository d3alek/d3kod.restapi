from Products.PloneTestCase import ptc

from collective.testcaselayer import ptc as tcl_ptc
from collective.testcaselayer import common

from Products.Five.testbrowser import Browser

class Layer(tcl_ptc.BasePTCLayer):
    """Install d3kod.restapi"""

    def afterSetUp(self):
        from Testing.ZopeTestCase import installPackage
        installPackage('d3kod.restapi')

        from d3kod.restapi import tests
        self.loadZCML('configure.zcml', package=tests)

        self.addProfile('d3kod.restapi:default')

        self.browser = Browser()

        self.browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()


        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising


layer = Layer([common.common_layer])
