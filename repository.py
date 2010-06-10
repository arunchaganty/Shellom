#!/usr/bin/env python

# Author - Vikram Rao S
# Date - 09-06-2010
# Purpose - This file is a repository of snippets currently installed in the
# computer

import tasks
Snippet=tasks.Snippet

allSnippets={}

class A(Snippet) :
    sname='The Snippet called A'
    sname='A'
    ID=1
    details=[ 'Give me a1', 'Give me a2', 'Give me a3' ]
    tags=[ 'a1', 'a2', 'a3' ]
    defaults=[ 'a1d', 'a2d', 'a3d' ]
    errors=['a1e', 'a2e', 'a3e' ]

    def validateInputs(inputs) :
        return True

allSnippets[A.sname]=A

# ---------------------------------------------------------------



class B(Snippet) :

    sname='The Snippet called B'
    sname='B'
    ID=1
    details=[ 'Give me b1', 'Give me b2', 'Give me b3' ]
    tags=[ 'b1', 'b2', 'b3' ]
    defaults=[ 'b1d', 'b2d', 'b3d' ]
    errors=['b1e', 'b2e', 'b3e' ]

    def validateInputs(inputs) :
        return True

allSnippets[B.sname]=B

# ---------------------------------------------------------------


class C(Snippet) :
    sname='The Snippet called C'
    sname='C'
    ID=1
    details=[ 'Give me c1', 'Give me c3', 'Give me c3' ]
    tags=[ 'c1', 'c2', 'c3' ]
    defaults=[ 'c1d', 'c2d', 'c3d' ]
    errors=['c1e', 'c2e', 'c3e' ]

    def validateInputs(inputs) :
        return True

allSnippets[C.sname]=C

# ---------------------------------------------------------------


