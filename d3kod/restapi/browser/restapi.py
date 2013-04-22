# -*- coding: utf-8 -*-

import json
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from five import grok
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone import api
from dehtml import dehtml

import logging

logger = logging.getLogger('Plone')

INVALID_QUERY_ERROR = "Invalid query"

@implementer(IPublishTraverse)
class RESTAPI(grok.View):
    """A view that exposes plone.api using JSON.
    """

    grok.context(INavigationRoot)
    grok.name('restapi')
    #grok.require('cmf.ManagePortal')

    apimod = None
    apimet = None
    contentFilter = dict()
    error = None


    def publishTraverse(self, request, name):
        logger.info("publishTraverse " + request['URL']+ " " +
                    json.dumps(name) + " " + json.dumps(self.error));
        if self.error is not None:
            return self
        if self.contentFilter.get('portal_type', None) is None:
            converted_name = self._convert_to_type(name)
            if converted_name == None:
                self.error = 'Invalid syntax: ' + name
                return self
            self.contentFilter['portal_type'] = converted_name 
            return self
        elif self.contentFilter.get('id', None) is None:
            self.contentFilter['id'] = name
            return self
        self.error = INVALID_QUERY_ERROR 
        return self

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

        self.request.response.setHeader("Content-type", "application/json")

        logger.info("render " + json.dumps(self.contentFilter) + " " +
                    json.dumps(str(type(self))))

        contentFilter = dict(self.contentFilter)
        self.contentFilter.clear()

#        if len(contentFilter) == 0:
            #self.error = INVALID_QUERY_ERROR

        if self.error is not None:
            return self._make_json_error(self.error)

        catalog = api.portal.get_tool(name='portal_catalog')
        queryResult = catalog(contentFilter)

        logger.info("queryResult " + json.dumps(str(queryResult)))

        if len(queryResult) == 0:
            return self._make_json_error("No results")

        detailsLevel = len(contentFilter)  

        output = [] 
        for brain in queryResult:
            output.append(self._make_output(brain.getObject(),
                                                 detailsLevel))


        if detailsLevel == 1: 
            queryDescription = self._convert_from_type(contentFilter['portal_type'])
            output = {queryDescription:output}

        output = json.dumps(output)

        return output

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




