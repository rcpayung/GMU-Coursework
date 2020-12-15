# hmm2.py

from numpy import zeros

# hardcode a system
def TrialSystem():
    # emission HMM.  Each node has an emission dictionary, 
    # and a transition integer.  The HMM is a dictionary of
    # these nodes
    hmm = {}
    hmm[0] = ({'A':0.3, 'B':0.2, 'C':0.5 }  , 1 )
    hmm[1] = ({ 'A':0.1, 'B':0.8, 'C':0.1} , 2) 
    hmm[2] = ({ 'A':0.4, 'B':0.6} , -1 ) 
    return hmm


# Emission HMM Recall
def ERecall( hmm, strng ):
    # strng is the input data string
    prb = 1 # initialization
    N = len( strng )
    for i in range( N ):
        if hmm[i][0].has_key( strng[i] ):
            prb *= hmm[i][0][ strng[i] ]
        else:
            prb = 0
            break
    return prb
    
def SimpleTHMM( ):
    hmm = {}
    hmm['begin'] = ('',{0:1.0} )
    hmm[0] = ('A', {1:0.3,2:0.7} )
    hmm[1] = ('B', {3:1.0} )
    hmm[2] = ('C', {3:1.0} )
    hmm[3] = ('D', {'end':1.0} )
    hmm['end'] = ('',{} )
    return hmm

def NextNode( hmm, k, ask ):
    t = hmm[k][1].keys() # transition for this node
    hit = []
    for i in t:
        if hmm[i][0]==ask:
            hit = i, hmm[k][1][i]
            break
    return hit

def TProb( hmm, instr ):
    L = len( instr )
    pbs = 1.0
    k = 'begin'
    for i in range( L ):
        tran = NextNode( hmm,k,instr[i])
        k = tran[0]
        pbs *= tran[1]
    return pbs

def NodeTable( sts, abet):
    # sts is a list of data strings
    L = len( sts )  # the number of strings
    D = len( sts[0] )   # length of string
    A = len( abet )
    NT = zeros( (A,D),int )-1
    nodecnt = 0
    for i in range( D ):
        for j in range( L ):
            ndx = abet.index( sts[j][i] )
            if NT[ndx,i] ==-1:
                NT[ndx,i] = nodecnt
                nodecnt +=1
    return NT

def MakeNodes( sts, abet, weights, nodet ):
    L = len( sts )
    D = len( sts[0] )   # length of string
    hmm = {}
    for j in range( D-1):
        for i in range( L ):
            # current letter
            clet = sts[i][j]
            # next letter
            nlet = sts[i][j+1]
            # node associated with current letter
            cnode = nodet[ abet.index(clet), j ]
            # node associated with next letter
            nnode = nodet[ abet.index(nlet), j+1]
            # connect the nodes
            if hmm.has_key( cnode ):
                # transition has been seen before
                # adjust the transition
                if hmm[cnode][1].has_key( nnode ):
                    hmm[cnode][1][nnode] += weights[i]
                else:
                    hmm[cnode][1][nnode] = weights[i]
            else:
                # transition has not been seen before - make new one
                hmm[cnode]= ( clet ,{ nnode: weights[i] })
    return hmm


def Normalization( hmm ):
    t = hmm.keys()
    for i in t:
        sm = 0
        for j in hmm[i][1].keys():
            sm += hmm[i][1][j]
        for j in hmm[i][1].keys():
            hmm[i][1][j] /= sm

def Ends( hmm, sts, abet, weights, nodet ):
    # add begin node
    T = {}
    L = len( sts )
    for i in range(L):
        clet = sts[i][0] # first letter in string i
        nlet = sts[i][1]
        idt = nodet[ abet.index(clet) ,0]
        # Build dictionary for the BEGIN node
        if idt != -1:
            if T.has_key( idt ):
                T[ idt] += weights[i]
            else:
                T[ idt] = weights[i]
    hmm['begin'] = ( '', T )
    # add end node
    hmm['end'] = ('',{} )
    for i in range( L ):
        clet = sts[i][-1]
        idt = nodet[ abet.index(clet) ,-1]
        hmm[idt] = (clet,{'end':1})

