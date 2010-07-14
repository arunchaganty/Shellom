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
    details = [ 'Subject', 'From', 'To ( a comma-space separated list )', 'Path to message', 'Path to attachment' ]
    tags = [ 'subject', 'from', 'to','message', 'attachment' ]
    defaults = [ 'A Message', 'localhost@locahost', 'localhost@localhost','/dev/null', '' ]
    errors = [ '', '', '', '', '' ]
    types = [ '', '', '', 'path:r', '' ]
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

#allSnippets[ send_email.sname ] = send_email
