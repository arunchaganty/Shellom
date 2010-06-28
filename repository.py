#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 09-06-2010
# Purpose - This file is a repository of snippets currently installed in the
# computer

import tasks, os, random, re
import Image # Resize Image needs this.
import urllib2 # download_pictures needs this
from BeautifulSoup import BeautifulSoup # download_pictures needs this

Snippet = tasks.Snippet

allSnippets = {}

class A(Snippet) :
    name = 'The Snippet called A'
    sname = 'A'
    ID = -3
    details = [ 'Give me a1', 'Give me a2', 'Give me a3' ]
    tags = [ 'a1', 'a2', 'a3' ]
    defaults = [ 'a1d', 'a2d', 'a3d' ]
    errors = ['a1e', 'a2e', 'a3e' ]

    def validateInputs(self, inputs) :
        return True

    def __init__(self) :
        pass

allSnippets[A.sname] = A

# ---------------------------------------------------------------



class B(Snippet) :

    name = 'The Snippet called B'
    sname = 'B'
    ID = -2
    details = [ 'Give me b1', 'Give me b2', 'Give me b3' ]
    tags = [ 'b1', 'b2', 'b3' ]
    defaults = [ 'b1d', 'b2d', 'b3d' ]
    errors = ['b1e', 'b2e', 'b3e' ]

    def validateInputs(self, inputs) :
        return True

    def __init__(self) :
        pass

allSnippets[B.sname] = B

# ---------------------------------------------------------------


class C(Snippet) :
    name = 'The Snippet called C'
    sname = 'C'
    ID = 0
    details = [ 'Give me c1', 'Give me c3', 'Give me c3' ]
    tags = [ 'c1', 'c2', 'c3' ]
    defaults = [ 'c1d', 'c2d', 'c3d' ]
    errors = ['c1e', 'c2e', 'c3e' ]

    def validateInputs(self, inputs) :
        return True

    def __init__(self) :
        pass

allSnippets[C.sname] = C

# ---------------------------------------------------------------

class clip2file( Snippet ) :
    name = 'Paste the contents of the clipboard into a file'
    sname = 'CLIP2FILE'
    ID = 1
    details = [ 'Output file' ]
    tags = [ 'outfile' ]
    default = [ 'clip2file'+str( random.randint( 1,10000 ) ) ]
    errors = [ '' ]

    def validateInputs( self,inputs ) :
        return True

    def doJob( self, inputs ) :
        os.system( 'xclip -o -selection clipboard > %s'%( inputs[ 0 ] ) )

allSnippets[ clip2file.sname ] = clip2file

# ---------------------------------------------------------------

class text2wave( Snippet ) :
    name = 'Convert the text in a file to a wav sound file'
    sname = 'TEXT2WAV'
    ID = 2
    details = [ 'Input file', 'Output file' ]
    tags = [ 'infile', 'outfile' ]
    default = [ '/dev/null', 'text2wave'+str( random.randint( 1,10000 ) ) ]
    errors = [ '', '' ]

    def validateInputs( self,inputs ) :
        return True

    def doJob( self, inputs ) :
        os.system( 'text2wave < "%s" > "%s"'%( inputs[ 0 ], inputs[ 1 ] ) )

allSnippets[ text2wave.sname ] = text2wave

# ---------------------------------------------------------------

class resize_image( Snippet ) :
    name = 'Resize an image to a given percentage or size'
    sname = 'RESIZE'
    ID = 3
    details = [ 'Input Image', 'Resize yyy% or yyyxyyy', 'Output file' ]
    tags = [ 'infile', 'factor', 'outfile' ]
    default = [ '/dev/null', '100%', 'resize'+str( random.randint( 1,10000 ) ) ]
    errors = [ 'Input image not found', 'Wrong resize factor format. Type, for example as 64% or 640x480.', '' ]

    def validateInputs( self, inputs ) :
        err=[]
        if not os.access( inputs[0], os.R_OK ) :
            err.append( 0 )
        #if not os.access( inputs[2], os.W_OK ) :
        #    err.append( 2 )
        if type( inputs[1] ) != str or len( inputs[1] ) == 0 or not ( re.match( '^\d+%$',inputs[1] ) or re.match('^\d+x\d+$', inputs[1] ) ) :
            err.append( 1 )
        return err

    def doJob( self, inputs ) :
        if re.match( '^\d+%$',inputs[1] ) :
            factor=int( inputs[1][:-1] )
            temp=int(inputs[1][:-1])
            temp=Image.open( inputs[0] ).size
            cmd='%dx%d'%( factor*temp[0]/100.0, factor*temp[1]/100.0 )
        elif re.match('^\d+x\d+$', inputs[1] ) :
            cmd = inputs[1]
        
        it=self.validateInputs( inputs )
        if it :
            print it
        else :
#            print 'convert %s -resize %s %s'%( inputs[0], cmd, inputs[2] )
            os.system( 'convert %s -resize %s %s'%( inputs[0], cmd, inputs[2] ) )

allSnippets[ resize_image.sname ] = resize_image

# ---------------------------------------------------------------

class screenshot( Snippet ) :
    name = 'Take a screenshot of the entire screen'
    sname = 'SCREENSHOT'
    ID = 4
    details = [ 'Delay in seconds', 'Output image file' ]
    tags = [ 'delay', 'outfile' ]
    default = [ '0', 'screenshot'+str( random.randint( 1,10000 ) ) ]
    errors = [ '', '' ]

    def validateInputs ( self, inputs ) :
        if len( inputs ) < 2 :
            return False
        return re.match('^\d+$',inputs[0] )

    def doJob( self, inputs ) :
        if self.validateInputs( inputs ) :
            os.system( 'sleep %s; import -window root %s'%( inputs[0], inputs[1] ) )
        else :
            print 'Error'

allSnippets[ screenshot.sname ] = screenshot

# ---------------------------------------------------------------

class download_pictures( Snippet ) :
    name = 'Download all pictures from a webpage'
    sname = 'DOWNLOAD_PICTURES'
    ID = 5
    details = [ 'URL of webpage', 'Folder to store images in' ]
    tags = [ 'url', 'folder' ]
    default = [ 'http://www.google.com/', 'download_pictures'+str( random.randint( 1,10000 ) ) ]
    errors = [ '', '' ]

    def validateInputs( self, inputs ) :
        return True

    def doJob( self, inputs ) :
        # os.system('if [ ! -d %s ] then; mkdir %s; fi'%( inputs[1], inputs[1] ) )
        if not os.access( inputs[1], os.W_OK ) :
            os.mkdir( inputs[1] )
        page = urllib2.urlopen( inputs[0] )
        soup = BeautifulSoup( page.read() )
        images = filter( lambda x: x[ 'src' ][0]=='/', soup.findAll( 'img' ) )
        ctr = 0
        for i in images :
            temp=urllib2.urlopen( inputs[0]+i[ 'src' ] )
            x=open( inputs[1]+'/pic%d'%( ctr ), 'w' )
            x.write( temp.read() )
            x.close()
            ctr+=1

allSnippets[ download_pictures.sname ] = download_pictures

# ---------------------------------------------------------------
