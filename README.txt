Introduction
============

A draft REST API addon for Plone.

Written by Aleksandar Kodzhabashev for "GSoC 2013 Plone REST API and Mobile Web
App" idea proposal

What works:
----------
 * HTTP GET requests

Sample usage:
------------
    GET <plone>/@@rest
returns a JSON decription of the root object

    GET <plone>/<page>/@@rest
returns a JSON description of page

    GET <plone>/<folder>/@@rest/list
returns a JSON array with the contents of <folder>
