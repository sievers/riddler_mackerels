import numpy as np

def read_file(fname='state_names.txt'):
    f=open(fname)
    lines=f.readlines()
    f.close()
    iref=ord('a')
    n=len(lines)
    lets=np.zeros([n,26])
    lens=np.zeros(n)
    for i in range(n):
        lines[i]=lines[i].strip()
        ll=lines[i].lower()
        for j in range(len(ll)):
            ind=ord(ll[j])-iref
            if (ind>=0)&(ind<26):
                lets[i][ind]=1
        lens[i]=len(ll)
    return lets,lens,lines

states,state_lens,state_names=read_file('state_names.txt')
words,word_lens,word_names=read_file('word.list.txt')
overlap=np.dot(words,states.T) #this is an nstate by nword matrix that will be zero iff no letters are in common
overlap=0+overlap>0 #replace the matrix product by a boolean array that's true iff there's letters in common
isunique=np.sum(overlap,axis=1)==overlap.shape[1]-1 #find all rows where only a single element is false
isunique=np.where(isunique)[0]
lens_unique=word_lens[isunique]
inds=np.where(lens_unique==lens_unique.max())[0]
for ind in inds:
    ii=isunique[ind]
    jj=np.where(overlap[ii,:]==False)[0][0]
    print(word_names[ii]+' shares no letters with ' + state_names[jj])

tmp=overlap[isunique,:] #pull the entries out of the matrix that have only one state
n_by_state=np.sum(tmp==False,axis=0)
for i in range(len(state_names)):
    if n_by_state[i]>0:
        print(state_names[i]+' has ' + repr(n_by_state[i]) + ' mackerels.')
    else:
        print(state_names[i]+' has no mackerels.')

