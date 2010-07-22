# Author - Vikram Rao S
# Date - 02-07-10
# Purpose - This module has functions for validating various types of inputs

import os, re, sys
sys.dont_write_bytecode = True

def exists( soup, file ) :
    return os.access( file, os.F_OK )

def RW( soup, file, access ) :
    permission = map( lambda x: getattr( os, x.upper()+'_OK' ), access )
    returnValue = True
    for i in permission :
        returnValue = returnValue and os.access( file, i )

    return returnValue

def pattern( soup, field, regex ) :
    return re.match( regex, field )

def isInt( soup, posNum ) :
    return re.match( '\d+', posNum )

def pathW( soup, field ) :
    result = os.access( field, os.W_OK ) or os.access( '/'.join(field.split('/')[:-1]), os.W_OK )
    result = result or ( field in [ x.string for x in soup.findAll( id=re.compile( 'o\d+' ) ) ] )
    return result

def pathR( soup, field ) :
    result = os.access( field, os.R_OK )
    if not result :
        result = result or ( field in [ x.string for x in soup.findAll( id=re.compile( 'o\d+' ) ) ] )
    return result

v = { 'exists' : exists, 'integer' : isInt, 'path:r' : pathR, 'path:w' : pathW }

def validator( type, soup, field ) :
    if type == 'exists' :
        return exists( soup, field )
    elif type == 'integer' :
        return isInt( soup, field )
    elif type == 'path:r' :
        return pathR( soup, field )
    elif type == 'path:w' :
        return pathW( soup, field )
    elif type[:7] == 'pattern' :
        return pattern( soup, field, type.split(':')[1] )
