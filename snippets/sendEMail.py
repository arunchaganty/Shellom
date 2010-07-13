#import smtplib, os
#from email.mime.image import MIMEImage
#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart
try :
    import smtplib, os
    from email.mime.image import MIMEImage
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
except ImportError :
    print "Couldn't import one or more of smtplib, os, email.mime.image.MIMEImage, email.mime.text.MIMEText and email.mime.multipart.MIMEMultipart."

class sendEMail() :
    name = 'Email a text message along with one attachment'
    sname = 'sendEMail'
    ID = 8
    details = [ 'Subject', 'From', 'Path to message', 'Path to attachment', 'To ( a comma-space separated list )' ]
    tags = [ 'subject', 'from','message', 'attachment', 'to' ]
    defaults = [ 'A Message', 'localhost@locahost','/dev/null', '' ,'localhost@localhost' ]
    errors = [ '', '', '', '', '' ]
    types = [ '', '',  'path:r', '', '' ]
    packages = [ 'sendmail' ]

    def __init__( self ) :
        try :
        	import smtplib, os
        	from email.mime.image import MIMEImage
        	from email.mime.text import MIMEText
        	from email.mime.multipart import MIMEMultipart
        except ImportError :
            print "Couldn't import one or more of smtplib, os, email.mime.image.MIMEImage, email.mime.text.MIMEText and email.mime.multipart.MIMEMultipart."

    def validateInputs( self, inputs ) :
        #return True
        return ( not inputs[2] ) or os.access( inputs[2], os.R_OK ) #and ( inputs[4] == '' or os.access( inputs[4]. os.R_OK ) )

    def doJob( self, inputs ) :
        msg = MIMEMultipart()
        if inputs[2] :
            msgText = open( inputs[2], 'rb' )
        # msg.preamble = msgText.read()
            msg.attach( MIMEText( msgText.read() ) )
            msgText.close()

        msg[ 'Subject' ] = inputs[0]
        msg[ 'From' ] = inputs[1]
        msg[ 'To' ] = ', '.join( [ x.strip() for x in inputs[4].split(',') ] )

        if inputs[3] != None and inputs[3].strip() != '' :
            attachment = open( inputs[3], 'rb' )
            img = MIMEImage( attachment.read() )
            attachment.close()
            msg.attach( img )

        s = smtplib.SMTP()
        s.connect()
        s.sendmail( msg[ 'From' ], msg[ 'To' ].split( ', '), msg.as_string() )
        s.quit()

#allSnippets[ send_email.sname ] = send_email
