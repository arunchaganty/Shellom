
#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 08-06-2010
# Purpose - This module defines a snippet and supports adding of snippets to a
# repository

import os, sys
sys.dont_write_bytecode = True

#__all__ = [ 'add_song_to_playlist',
#        'mount_disc_image',
#        'send_email',
#        'clip2file',
#        'publish_wordpress_post',
#        'text2wav',
#        'download_pictures',
#        'resize_image',
#        'screenshot' ]

for module in os.listdir( os.path.dirname( __file__ ) ) :
    if module == '__init__.py' or  module[-3:] != '.py' :
        continue
    __import__( module[:-3] , locals(), globals() )
