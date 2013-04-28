# -*- coding: utf-8 -*-

import json
from collective.jsonify import get_item, get_children
from zope.interface import implementer
from five import grok
from plone.app.layout.navigation.interfaces import Interface, INavigationRoot
from plone import api
from d3kod.restapi.browser.restapi import RESTAPI, getObjectPath, makeJsonError

import logging

logger = logging.getLogger('Plone')

INVALID_QUERY_ERROR = "Invalid query"


class GET(grok.View):
    """A view that exposes plone.api using JSON.
    """

    grok.context(RESTAPI)
    grok.name('get')
    
    def render(self):
        """ Return an appropriate JSON response 
        """
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
                return makeJsonError('Object not found.')
            objectAtPath = objectAtPath[0].getObject()

        logger.info('form is ' + str(self.request.form))

        if 'list' in self.request.form:
            return get_children(objectAtPath)

        return get_item(objectAtPath)

