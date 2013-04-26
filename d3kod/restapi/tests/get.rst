===================================
Functional doctest of GET responses
===================================

HTTP GET @@rest returns a JSON response with the root site
object description
    >>> from Products.Five.testbrowser import Browser
    >>> self.browser = Browser()
    >>> self.browser.open(self.portal.absolute_url() + '/@@rest')
    >>> self.browser.headers['Content-type']
    'application/json' 
    >>> import json
    >>> from plone import api
    >>> decodedContents = json.loads(self.browser.contents)
    >>> decodedContents['_path'] == '/'+api.portal.get().virtual_url_path()
    True

HTTP GET <page>/@@rest returns the object description of the
page with id=<page>	
    >>> from plone import api
    >>> catalog = api.portal.get_tool('portal_catalog')
    >>> samplePage = catalog(portal_type='Document')[0]
    >>> samplePagePath = samplePage.getPath()
    >>> from Products.Five.testbrowser import Browser
    >>> self.browser = Browser()
    >>> self.browser.open(self.portal.absolute_url())
    >>> self.browser.open(samplePagePath + '/@@rest')
    >>> import json
    >>> decodedContents = json.loads(self.browser.contents)
    >>> decodedContents['_path'] == samplePagePath
    True

HTTP GET <object>@@rest/list lists the contents of an object (surprise!) if it is a
container. If not, returns an error
    >>> from plone import api 
    >>> catalog = api.portal.get_tool('portal_catalog')
    >>> sampleFolder = catalog(portal_type='Folder')[1]
    >>> sampleFolderPath = sampleFolder.getPath()
    >>> sampleFolderChild = catalog(path={'query':sampleFolderPath, 'depth':1})[0]
    >>> from Products.Five.testbrowser import Browser
    >>> self.browser = Browser()
    >>> self.browser.open(self.portal.absolute_url())
    >>> self.browser.open(sampleFolderPath + '/@@rest/list')
    >>> import json
    >>> decodedContents = json.loads(self.browser.contents)
    >>> sampleFolderChild.id in decodedContents
    True

Horray! This is all the GET functionallity.
