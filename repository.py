#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 09-06-2010
# Purpose - This file is a repository of snippets currently installed in the
# computer

import tasks
import os
import random
Snippet=tasks.Snippet

allSnippets={}

class A(Snippet) :
    name='The Snippet called A'
    sname='A'
    ID=1
    details=[ 'Give me a1', 'Give me a2', 'Give me a3' ]
    tags=[ 'a1', 'a2', 'a3' ]
    defaults=[ 'a1d', 'a2d', 'a3d' ]
    errors=['a1e', 'a2e', 'a3e' ]

    def validateInputs(self, inputs) :
        return True

    def __init__(self) :
        pass

allSnippets[A.sname]=A

# ---------------------------------------------------------------



class B(Snippet) :

    name='The Snippet called B'
    sname='B'
    ID=0
    details=[ 'Give me b1', 'Give me b2', 'Give me b3' ]
    tags=[ 'b1', 'b2', 'b3' ]
    defaults=[ 'b1d', 'b2d', 'b3d' ]
    errors=['b1e', 'b2e', 'b3e' ]

    def validateInputs(self, inputs) :
        return True

    def __init__(self) :
        pass

allSnippets[B.sname]=B

# ---------------------------------------------------------------


class C(Snippet) :
    name='The Snippet called C'
    sname='C'
    ID=0
    details=[ 'Give me c1', 'Give me c3', 'Give me c3' ]
    tags=[ 'c1', 'c2', 'c3' ]
    defaults=[ 'c1d', 'c2d', 'c3d' ]
    errors=['c1e', 'c2e', 'c3e' ]

    def validateInputs(self, inputs) :
        return True

    def __init__(self) :
        pass

allSnippets[C.sname]=C

# ---------------------------------------------------------------

class clip2file( Snippet ) :
    name='Paste the contents of the clipboard into a file'
    sname='CLIP2FILE'
    ID=1
    details=[ 'Output file' ]
    tags=[ 'outfile' ]
    default=[ 'clip2file'+str( random.randint( 1,10000 ) ) ]
    errors=[ '' ]

    def validateInputs( self,inputs ) :
        return True

    def doJob( self, inputs ) :
        os.system( 'xclip -o -selection clipboard > %s'%( inputs[ 0 ] ) )

allSnippets[ clip2file.sname ] = clip2file

# ---------------------------------------------------------------

class text2wave( Snippet ) :
    name='Convert the text in a file to a wav sound file'
    sname='TEXT2WAV'
    ID=2
    details=[ 'Input file', 'Output file' ]
    tags=[ 'infile', 'outfile' ]
    default=[ '/dev/random', 'text2wave'+str( random.randint( 1,10000 ) ) ]
    errors=[ '', '' ]

    def validateInputs( self,inputs ) :
        return True

    def doJob( self, inputs ) :
        os.system( 'text2wave < "%s" > "%s"'%( inputs[ 0 ], inputs[ 1 ] ) )

allSnippets[ text2wave.sname ] = text2wave

# ---------------------------------------------------------------
