#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 06-08-2010
# Purpose - This module generates xml content for a given snippet and a list of inputs
# output, we can just return this 'pointer'.

# IMPORTANT : CHANGED - Recursive XML scan supprts both input and output finding. The assumption
# is that the last input to any snippet is actually a file name or anything else
# that points to the snippet's output. So when some other snippet asks for it's
# TO CHANGE - getxml() currently assumes that every snippet has a default. Think
# about the assumption and change accordingly.

from tasks import *
from BeautifulSoup import BeautifulStoneSoup

def aux( oldid, soup ) :
    """Recursively find a previous input or output from an XML soup."""

    prev=soup.find( id=oldid ).string.strip()

    if len(prev)==0 :
        return 'ERROR'

    if prev[0]!='~' :
        return prev


def getxml( xml, snippet, inputs, snip, inp ) :
    """Generates the XML string for encoding a snippet and its inputs.
    @param snip - the ID to give to the snippets
    @param inp - the ID to give to the first input
    """
    
    
    if len( inputs )!=len( snippet.tags ) :
        return list('ERROR')
    
    for i in range( 1, len( inputs ) ) :
        if inputs[i]=='' :
            inputs[i]=snippet.defaults[i]

    xml.append( '<%s snipID="%d" id="s%d">\n'%( snippet.sname, snippet.ID, snip ) )
    
    for i in range( len( inputs ) ) :
        inn=inputs[i].strip()

        if i==len( inputs )-1 :
            iORo='o'
        else :
            iORo='i'
       
        if inn[0]!='~' :
            xml.append( '<%s id="%s%d">%s</%s>\n'%( snippet.tags[i], iORo, inp, inputs[i], snippet.tags[i] ) )
            inp+=1
        else :
            soup=BeautifulStoneSoup( ''.join( xml ) )
        
            toBeAppended =  aux( inn[1:], soup )

            if toBeAppended=='ERROR' :
                return list('ERROR')
            else :
                xml.append( '<%s id="%s%d">%s</%s>\n'%( snippet.tags[i], iORo, inp, toBeAppended, snippet.tags[i] ) )
                inp+=1

    xml.append( '</%s>'%( snippet.sname  )  )
    return  xml
