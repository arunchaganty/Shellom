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
import os
from BeautifulSoup import BeautifulStoneSoup
import validators

def aux( oldid, soup ) :
    """Recursively find a previous input or output from an XML soup."""

    prev=soup.find( 'field', id=oldid ).string.strip()

    if len(prev) == 0 :
        return 'ERROR_INTERLEAVING'

    if prev[0] != '~' :
        return prev.strip()


def getxml( xml, snippet, inputs, snip, inp ) :
    """Generates the XML string for encoding a snippet and its inputs.
    @param snip - the ID to give to the snippets
    @param inp - the ID to give to the first input
    """
    
    copyOfXML = xml
    
    if len( inputs ) != len( snippet.tags ) :
        return list('ERROR_TOO_FEW_INPUTS')
    
    for i in range( len( inputs ) ) :
        if inputs[i] == '' :
            inputs[i] = snippet.defaults[i]
        if snippet.types[i] in [ 'path:r', 'path:w' ] and inputs[i] != '' and ( inputs[i][0] not in [ '/', '~' ] ):
            inputs[i] = os.getcwd()+'/'+inputs[i]#os.path.abspath( inputs[i] )

    xml.append( '<snippet task="%s" snipID="%d" id="s%d">\n'%( snippet.sname, snippet.ID, snip ) )
    
    for i in range( len( inputs ) ) :
        inn=inputs[i].strip()
        soup = BeautifulStoneSoup( ''.join( xml ) )

        
        if i == len( inputs )-1 :
            iORo = 'o'
        else :
            iORo = 'i'
       
        if len( inn ) == 0 or inn[0] != '~' :
            toBeAppended = inputs[i]
            #xml.append( '<field task="%s" id="%s%d">%s</field>\n'%( snippet.tags[i], iORo, inp, inputs[i] ) )
        elif inn[0] == '~' :
            try :
                toBeAppended =  str( aux( inn[1:], soup ) )
            except BaseException :
                xml = copyOfXML
                return list( 'ERROR_INTERLEAVING' )

            if toBeAppended == 'ERROR_INTERLEAVING' :
                xml = copyOfXML
                return list('ERROR_INTERLEAVING')
            #else :
                #xml.append( '<field task="%s" id="%s%d">%s</field>\n'%( snippet.tags[i], iORo, inp, toBeAppended) )
        if snippet.types[i] != '' and inputs[i] != '' :
            if not validators.validator( snippet.types[i], soup, toBeAppended ) :
                xml = copyOfXML
                return list( 'ERROR_INVALID_INPUT:%s\n%s'%( snippet.tags[i], toBeAppended ) )

        xml.append( '<field task="%s" id="%s%d">%s</field>\n'%( snippet.tags[i], iORo, inp, toBeAppended ) )
        inp += 1

    xml.append( '</snippet>'  )
    return  xml
