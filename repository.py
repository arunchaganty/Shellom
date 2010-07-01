#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 09-06-2010
# Purpose - This file is a repository of snippets currently installed in the
# computer

import tasks, os, random, re
import Image # Resize Image needs this.
import urllib2 # download_pictures needs this
from BeautifulSoup import BeautifulSoup # download_pictures needs this
import pexpect # Mount image needs this
import smtplib                                 # Send email needs This 
from email.mime.image import MIMEImage         # Send email needs This 
from email.mime.text import MIMEText           # Send email needs This 
from email.mime.multipart import MIMEMultipart # Send email needs This     
import wordpresslib # Publish wordpress post needs this

Snippet = tasks.Snippet

allSnippets = {}

# class A(Snippet) :
#     name = 'The Snippet called A'
#     sname = 'A'
#     ID = -3
#     details = [ 'Give me a1', 'Give me a2', 'Give me a3' ]
#     tags = [ 'a1', 'a2', 'a3' ]
#     defaultss = [ 'a1d', 'a2d', 'a3d' ]
#     errors = ['a1e', 'a2e', 'a3e' ]
# 
#     def validateInputs(self, inputs) :
#         return True
# 
#     def __init__(self) :
#         pass
# 
# allSnippets[A.sname] = A

# ---------------------------------------------------------------

class clip2file( Snippet ) :
    name = 'Paste the contents of the clipboard into a file'
    sname = 'CLIP2FILE'
    ID = 1
    details = [ 'Output file' ]
    tags = [ 'outfile' ]
    defaults = [ 'clip2file'+str( random.randint( 1,10000 ) ) ]
    errors = [ '' ]

    def validateInputs( self,inputs ) :
        return True
        #return os.access( inputs[ 0 ] , os.F_OK ) and not os.access( inputs[ 0 ], os.W_OK )

    def doJob( self, inputs ) :
        os.system( 'xclip -o -selection clipboard >> %s'%( inputs[ 0 ] ) )

allSnippets[ clip2file.sname ] = clip2file

# ---------------------------------------------------------------

class text2wave( Snippet ) :
    name = 'Convert the text in a file to a wav sound file'
    sname = 'TEXT2WAV'
    ID = 2
    details = [ 'Input file', 'Output file' ]
    tags = [ 'infile', 'outfile' ]
    defaults = [ '/dev/null', 'text2wave'+str( random.randint( 1,10000 ) ) ]
    errors = [ '', '' ]

    def validateInputs( self,inputs ) :
        return True
        #return os.access( inputs[ 1 ] , os.F_OK ) and not os.access( inputs[ 1 ], os.W_OK )

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
    defaults = [ '/dev/null', '100%', 'resize'+str( random.randint( 1,10000 ) ) ]
    errors = [ 'Input image not found', 'Wrong resize factor format. Type, for example as 64% or 640x480.', '' ]

    def validateInputs( self, inputs ) :
        return True
        err=[]
        if not os.access( inputs[0], os.R_OK ) :
            err.append( 0 )
        if os.access( inputs[2], os.F_OK ) and not os.access( inputs[2], os.W_OK ) :
            err.append( 2 )
        if type( inputs[1] ) != str or not ( re.match( '^\d+%$',inputs[1] ) or re.match('^\d+x\d+$', inputs[1] ) ) :
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
        
        #it=self.validateInputs( inputs )
        #if it :
        #    print it
        #else :
        os.system( 'convert %s -resize %s %s'%( inputs[0], cmd, inputs[2] ) )

allSnippets[ resize_image.sname ] = resize_image

# ---------------------------------------------------------------

class screenshot( Snippet ) :
    name = 'Take a screenshot of the entire screen'
    sname = 'SCREENSHOT'
    ID = 4
    details = [ 'Delay in seconds', 'Output image file' ]
    tags = [ 'delay', 'outfile' ]
    defaults = [ '0', 'screenshot'+str( random.randint( 1,10000 ) ) ]
    errors = [ '', '' ]

    def validateInputs ( self, inputs ) :
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
    defaults = [ 'http://www.google.com/', 'download_pictures'+str( random.randint( 1,10000 ) ) ]
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

class mount_disc_image( Snippet ) :
    name = 'Mount an ISO or UDF disc image'
    sname = 'MOUNT_DISC_IMAGE'
    ID = 6
    details = [ 'Path to image', 'Path to mount point', 'Root password','Unmount ? y or Y for \'yes\' and anything else for \'no\'' ]
    tags = [ 'image', 'mountPoint', 'password', 'unmount' ]
    defaults = [ '', '/media/mount_image'+str( random.randint( 1,10000 ) ), '', 'n' ]
    errors = [ 'No image found', '', 'Wrong or no root password given', '' ]

    def validateInputs( self, inputs ) :
        return os.access( inputs[ 0 ], os.R_OK ) and not ( os.access( inputs[1], os.F_OK ) and not os.access( inputs[1], os.R_OK ) )

    def doJob( self, inputs ) :
        if inputs[3] in [ 'y', 'Y' ] :
            flag = 1
            command = 'sudo umount '+ inputs[1]
        else :
            flag = 0
            if not os.access( inputs[1], os.F_OK ) :
                os.mkdir( inputs[1] )
            #-----------------------------------------
            if inputs[0][-3:] in [ 'dmg', 'DMG' ] :
                imgType = '-t dmg'
            elif inputs[0][-3:] in [ 'iso', 'ISO' ] :
                imgType = '-t iso9660'
            else :
                imgType = ''
            #-----------------------------------------
            command = 'sudo mount %s %s %s'%( imgType, inputs[0], inputs[1] )

        if flag and not os.access( inputs[1], os.F_OK ) :  # Create mount point if it doesn't exist
            os.mkdir( inputs[1] )

        c = pexpect.spawn( command )
        c.sendline( inputs[2] )

allSnippets[ mount_disc_image.sname ] = mount_disc_image

# ---------------------------------------------------------------

class add_song_to_playlist( Snippet ) :
    name = 'Add a song to a playlist'
    sname = 'ADD_SONG_TO_PLAYLIST'
    ID = 7
    details = [ 'Path to song', 'Path to playlist' ]
    tags = [ 'song', 'playlist' ]
    defaults = [ '/dev/null', '/dev/null' ]
    errors = [ '', '' ]

    def validateInputs( self, inputs ) :
        return True
        return os.access( inputs[0], os.F_OK ) and os.access( '/'.join( inputs[1].split('/')[:-1] ), os.W_OK )

    def doJob( self, inputs ) :
        os.system( 'echo %s >> %s'%tuple( inputs ) )

allSnippets[ add_song_to_playlist.sname ] = add_song_to_playlist

# ---------------------------------------------------------------

class send_email( Snippet ) :
    name = 'Email a text message along with one attachment'
    sname = 'SEND_EMAIL'
    ID = 8
    details = [ 'Subject', 'From', 'To ( a comma-space separated list )', 'Path to message', 'Path to attachment' ]
    tags = [ 'subject', 'from', 'to','message', 'attachment' ]
    defaults = [ 'A Message', 'localhost@locahost', 'localhost@localhost','/dev/null', '' ]
    errors = [ '', '', '', '', '' ]

    def validateInputs( self, inputs ) :
        return True
        return os.access( inputs[3], os.R_OK ) #and ( inputs[4] == '' or os.access( inputs[4]. os.R_OK ) )

    def doJob( self, inputs ) :
        msgText = open( inputs[3], 'rb' )
        msg = MIMEMultipart()
        # msg.preamble = msgText.read()
        msg.attach( MIMEText( msgText.read() ) )
        msgText.close()

        msg[ 'Subject' ] = inputs[0]
        msg[ 'From' ] = inputs[1]
        msg[ 'To' ] = ', '.join( [ x.strip() for x in inputs[2].split(',') ] )

        if inputs[4].strip() != '' :
            attachment = open( inputs[4], 'rb' )
            img = MIMEImage( attachment.read() )
            attachment.close()
            msg.attach( img )

        s = smtplib.SMTP()
        s.connect()
        s.sendmail( msg[ 'From' ], msg[ 'To' ].split( ', '), msg.as_string() )
        s.quit()

allSnippets[ send_email.sname ] = send_email

# ---------------------------------------------------------------

    #    I am stuck because my present code doesn't handle unlimited inputs
    #    well. Specifically, there is no way of crosslinking with inputs of
    #    non-predetermined length.
    
class publish_wordpress_post( Snippet ) :
    name = 'Publish a wordpress blog post'
    sname = 'PUBLISH_WORDPRESS_POST'
    ID = 9
    details = [ 'Blog url', 'Username', 'Password', 'Subject', 'Path to Description', 'Media ( optional )' ]
    tags = [ 'blog', 'username', 'password', 'subject', 'description', 'media' ]
    defaults = [ '', '', '', 'A subject', 'Some words', '' ]
    errors = [ 'Blog fault', 'Username fault', 'Password fault', '', '', '' ]

    def validateInputs( self, inputs ) :
        return True

    def doJob( self, inputs ) :
        if inputs[0][-1] != '/' :
            inputs[0] = inputs[0] + '/'
            
        wp = wordpresslib.WordPressClient( inputs[0]+'xmlrpc.php', inputs[1], inputs[2] )
        wp.selectBlog( 0 )
        
        if inputs[-1] != '' :
            img = wp.newMediaObject( inputs[-1] )

        post = wordpresslib.WordPressPost()
        post.title = inputs[3]
        des = open( inputs[4], 'r' )
        post.description = ''

        if inputs[-1] :
            post.description = '<img src = "%s" /> <br/>'% img

        post.description += des.read()
        des.close()
        
        try :
            newPost = wp.newPost( post, True )

        except BaseException :
            print 'An error occured while accessing your blog'

allSnippets[ publish_wordpress_post.sname ] = publish_wordpress_post

# ---------------------------------------------------------------
