# -*- coding: utf-8 -*-

import json
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse
from five import grok
from plone.app.layout.navigation.interfaces import Interface, INavigationRoot
from plone import api
from dehtml import dehtml

import logging

logger = logging.getLogger('Plone')

INVALID_QUERY_ERROR = "Invalid query"

def getObjectPath(relPath):
    suffpos = relPath.find('@@rest')

    if suffpos == -1:
        if relPath[-1] == '/':
            return relPath[:-1]
        return relPath

    return relPath[:suffpos-1]

def makeJsonError(errorString): 
    return json.dumps({"type":"error", "message":errorString})

@implementer(IPublishTraverse)
class RESTAPI(grok.View):
    """A view that exposes plone.api using JSON.
    """

    grok.context(Interface)
    grok.name('rest')

    #grok.require('cmf.ManagePortal')

    error = None
    toList = False


    def publishTraverse(self, request, name):
        logger.info("publishTraverse " + request['URL']+ " " +
                    json.dumps(name) + " " + json.dumps(self.error));

        if self.error is not None:
            return self

        if name != 'list':
            self.error = INVALID_QUERY_ERROR
        else:
            self.toList = True

        return self

    def __init__(self, context, request):
       logger.info("in init " + str(request.PATH_INFO))
       self.context = context;
       self.request = request;
       if self.request.PATH_INFO[-1] != '/':
           self.request.PATH_INFO += '/';

    def _parse_list_path(self, path):
        listpos = path.rfind('list/')
        return path[:listpos]


    def render(self):
        """ 
        Return an appropriate JSON response depending on the HTTP method used
        """

        self.request.response.setHeader("Content-type", "application/json")

        if self.error is not None:
            return makeJsonError(self.error)

        if self.request.method == "GET":
            path = self.request.PATH_INFO
            if self.toList:
                self.request.form['list'] = True
                path = self._parse_list_path(path) 

            path += '@@get'
            logger.info('jumping to ' + path)
            get = self.context.restrictedTraverse(path)
            return get()
        else: 
            logger.info('request method is ' + self.request.method)
            return makeJsonError('Unsupported request')

