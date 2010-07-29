#import wordpresslib
try :
    import wordpresslib
except ImportError :
    print "Check if you have the wordpresslib Python module .\nGet it from http://www.blackbirdblog.it/download/software/wordpresslib.zip"

class publishWordpressPost() :
    name = 'Publish a wordpress blog post'
    sname = 'publishWordpressPost'
    ID = 9
    details = [ 'Blog url', 'Username', 'Password', 'Subject', 'Path to Description', 'Media ( optional )' ]
    tags = [ 'blog', 'username', 'password', 'subject', 'description', 'media' ]
    defaults = [ '', '', '', 'A subject', 'Some words', '' ]
    errors = [ 'Blog fault', 'Username fault', 'Password fault', '', '', '' ]
    types = [ '', '', '', '', 'path:w', '' ]
    packages = [ 'wordpresslib' ]

    def __init__( self ) :
        try :
        	import wordpresslib
        except ImportError :
            print "Couldn't import wordpresslib."

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

#allSnippets[ publish_wordpress_post.sname ] = publish_wordpress_post
