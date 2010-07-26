#import pexpect, random, os
try :
    import pexpect, random, os
except ImportError :
    print "Couldn't import one or more of pexpect, random and os."

class mountDiscImage() :
    name = 'Mount an ISO or UDF disc image'
    sname = 'mountDiscImage'
    ID = 6
    details = [ 'Path to image', 'Path to mount point', 'Root password','Unmount ? y or Y for \'yes\' and anything else for \'no\'' ]
    tags = [ 'image', 'mountPoint', 'password', 'unmount' ]
    defaults = [ '/dev/null', '/media/mount_image'+str( random.randint( 1,10000 ) ), '', 'n' ]
    errors = [ 'No image found', '', 'Wrong or no root password given', '' ]
    types = [ 'path:r', '', '', '' ]
    packages = []

    def __init__( self ) :
        try :
    	    import pexpect, random, os
        except ImportError :
            print "Couldn't import one or more of pexpect, random and os."

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
            command = 'sudo mount %s "%s" "%s"'%( imgType, inputs[0], inputs[1] )

        if flag and not os.access( inputs[1], os.F_OK ) :  # Create mount point if it doesn't exist
            os.mkdir( inputs[1] )

        c = pexpect.spawn( command )
        c.sendline( inputs[2] )

#allSnippets[ mount_disc_image.sname ] = mount_disc_image
