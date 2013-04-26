# -*- coding: utf-8 -*-

import json
from collective.jsonify import get_item, get_children
from zope.interface import implementer
from five import grok
from plone.app.layout.navigation.interfaces import Interface, INavigationRoot
from plone import api
from d3kod.restapi.browser.restapi import RESTAPI, getObjectPath 

import logging

logger = logging.getLogger('Plone')

INVALID_QUERY_ERROR = "Invalid query"


class RESTAPI(grok.View):
    """A view that exposes plone.api using JSON.
    """

    grok.context(RESTAPI)
    grok.name('get')
    
    #grok.require('cmf.ManagePortal')

    def _convert_to_type(self, userInput):
        if not userInput.endswith('s'):
            return None
        userInput = userInput.capitalize()[:-1]
        if userInput == 'Page':
            userInput = 'Document'
        return userInput

    def _convert_from_type(self, contentType):
        return contentType.lower()+'s'
        
    def render(self):
        """ Return an appropriate JSON response 
        """

#        if self.request.method == "GET":
            #self.context.restrictedTraverse('@@get')

        #logger.info("render " + json.dumps(self.contentFilter) + " " +
                    #json.dumps(str(type(self))))

        #contentFilter = dict(self.contentFilter)
        #self.contentFilter.clear()

        #if self.error is not None:
            #return self._make_json_error(self.error)

        #catalog = api.portal.get_tool(name='portal_catalog')
        #queryResult = catalog(contentFilter)

        #logger.info("queryResult " + json.dumps(str(queryResult)))

        #if len(queryResult) == 0:
            #return self._make_json_error("No results")

        #detailsLevel = len(contentFilter)  

        #output = [] 
        #for brain in queryResult:
            #output.append(self._make_output(brain.getObject(),
                                                 #detailsLevel))
        #if detailsLevel == 0:
            #output = {"site_contents":output}

        #elif detailsLevel == 1: 
            #queryDescription = self._convert_from_type(contentFilter['portal_type'])
            #output = {queryDescription:output}

        #output = json.dumps(output)
        logger.info('get path is ' + self.request.PATH_INFO + " " +
                    getObjectPath(self.request.PATH_INFO));

        catalog = api.portal.get_tool('portal_catalog')
        path = getObjectPath(self.request.PATH_INFO);
        if path.count('/') == 1:
            logger.info('get objectAtPath is portal')
            objectAtPath = api.portal.get()
        else:
            objectAtPath = catalog(path={'query':path, 'depth':0})
            logger.info('get objectAtPath is ' + str(objectAtPath))
            if len(objectAtPath) != 1:
                return self._make_json_error('Object not found.')
            objectAtPath = objectAtPath[0].getObject()

        return get_item(objectAtPath)

    def _make_json_error(self, errorString): 
        return json.dumps({"type":"error", "message":errorString})

    def _make_output(self, obj, detailsLevel):
        output = None
        if detailsLevel == 0:
            output = self._get_general_info(obj)
        if detailsLevel == 1:
            output = self._get_type_info(obj)
        elif detailsLevel == 2:
            if obj.portal_type == 'Document':
                output = self._get_doc_info(obj)

        return output

    def _get_general_info(self, obj):
        d = {}
        d['id'] = obj.id
        d['title'] = obj.title
        d['owner'] = obj.getOwner().getId()
        d['type'] = obj.portal_type
        return d


    def _get_type_info(self, obj):
        d = self._get_general_info(obj)
        d.pop('type')
        return d
        
    def _get_doc_info(self, obj):
        d = self._get_general_info(obj)
        fields = {}
        fields['description'] = obj.description
        fields['text'] = dehtml(obj.getText())
        d['fields'] = fields
        return d 




