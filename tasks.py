options=['A','B','C']
current={'A':0, 'B':0, 'C':0}
Alist=['a1','a2','a3']
Blist=['b1','b2','b3']
Clist=['c1','c2','c3']
lists={'A':Alist, 'B':Blist, 'C':Clist}

def getInput(option) :
	O=options[option]
	if current[O]<len(lists[O]):
		current[O]+=1
		return lists[O][current[O]-1]
	else :
		return '0'
