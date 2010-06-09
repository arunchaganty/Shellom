#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 06-08-2010
# Purpose - This module generates xml content for a given snippet and a list of inputs
# TO CHANGE - getxml() currently assumes that every snippet has a default. Think
# about the assumption and change accordingly.

import tasks
from BeautifulSoup import BeautifulStoneSoup

def auxinput( oldid, soup ) :
    """Recursively find a previous input from an XML soup."""

    prev=soup.find( id=oldid ).string.strip()

    if len(prev==0)
        return 'ERROR'

    if prev[0]!='~' :
        return prev

    if prev[1]=='o' :
        return auxoutput( prev[1:], soup )
    if prev[1]=='i' :
        return auxinput( prev[1:], soup )

def auxoutput( oldid, soup ) :
    """Recursively find a previous output from an XML soup."""
    
    prev=soup.find( id=oldid ).findChildren()[-1].string.strip()
    
    if len(prev==0)
        return 'ERROR'

    if prev[0]!='~' :
        return prev
    
    if prev[1]=='o' :
        return auxoutput( prev[1:], soup )
    if prev[1]=='i' :
        return auxinput( prev[1:], soup )

def getxml( snipID, inputs, snip, inp ) :
    """Generates the XML string for encoding a snippet and its inputs."""
    
    x=snippets[snipID]
    
    if len( inputs )!=len( x.tags ) :
        return 'ERROR'
    
    for i in xrange( 1, len( inputs )+1 ) :
        if inputs[i]=='' :
            inputs[i]=x.defaults[i]
    
    xml=['<%s snipID="%d" id="o%d">\n'%( x.sname, snipID, snip )]
    
    for i in xrange( 1, len( inputs )+1 ) :
        inn=inputs[i].strip()
        
        if not inn[0]=='~' :
            xml.append( '<%s id="i%d">%s</%s>\n'%( x.tags[i], inputs[i], inp, x.tags[i] ) )
            inp+=1
        else :
            soup=BeautifulStoneSoup( ''.join( xml ) )
            xml.append( aux( inn[1:], soup ) )
        
            if inn[1]=='o':
                toBeAppended = auxoutput( soup, inn[1:] )
            elif inn[1]=='i':
                toBeAppended =  auxinput( soup, inn[1:] )

            if toBeAppended=='ERROR' :
                return 'ERROR'
            else :
                xml.append( toBeAppended )
    
    return ''.join( xml )
