#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 08-06-2010
# Purpose - This module defines a snippet and supports adding of snippets to a
# repository

import os
import pickle

class Snippet :   

    name=''
    sname=''
    ID=0
    version=0
    details=[]
    tags=[]
    defaults=[]
    errors=[]

    def validateInputs( self, inputs ):
        pass

    def doJob( inputs ):
        pass

#    def assignJob( self, fn ):  # Redundant ... due to Python-style object.function = a_new_function assignments.
#        self.doJob=fn        # But this will remind me of the fact.

    def __init__( self, fn ):
        """ Creates a snippet with the given function as it's 'job'."""
        self.doJob=fn

def addSnippetToRepo( snip ):
    if snip.__class__==Snippet : # and len( snippets )<=snip.ID :
        snippets.append( snip )    # I should index by ID and check for duplicates etc. Will do it later. 

def executeForAll( snippet, listofinputs ) :
    for i in listofinputs :
        snippet.doJob( i )

#----------------------------------------------

sn=open( 'snippets.dump', 'r' )  # Check if the file exists. If not,  create one and let snippets be an empty list.
snippets=pickle.load( sn )
sn.close()
sn=open( 'snippets.dump', 'w' )
