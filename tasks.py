#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 08-06-2010
# Purpose - This module defines a snippet and supports adding of snippets to a
# repository

import os

repo=open('repository.py','a')

class Snippet :   

    name=''
    sname=''   # Short name. This will be used as the XML tag.
    ID=0
    version=0
    details=[]
    tags=[]
    defaults=[]
    errors=[]

    def validateInputs( inputs ):
        pass

    def doJob( inputs ):
        pass

    def __init__( self, fn ):
        """ Creates a snippet with the given function as it's 'job'."""
        self.doJob=fn

def executeForAll( snippet, listOfInputs ) :
    """Support for batch application of a snippet. The idea is still vague. """

    for i in listOfInputs :
        snippet.doJob( i )
