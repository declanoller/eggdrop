import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

N = 100

def Pmat(a,s1,s2):
    #I'll say that f=0 means solved and a=0 is going to the 'solved' state.
    #Translate from my states to more readable stuff.
    if s1==0:
        if s2==0:
            return(1)
        else:
            return(0)

    if s1>0 and s1<=N:
        e1 = 1
        f1 = s1
    if s1>N:
        e1 = 2
        f1 = s1 - N

    if s2==0:
        f2 = 0
        e2 = 0

    if s2>0 and s2<=N:
        e2 = 1
        f2 = s2
    if s2>N:
        e2 = 2
        f2 = s2 - N

    if e1==1:

        if a==0 and f2==0:
            return(1)
        else:
            return(0)

    else:
        if s2==0:
            return(0)
        d = a
        if d<=f1 and d>0:
            #This is if it's a drop in the suitable range, with the
            #two possibilities of breaking it or not.
            if f2==d and e2==1:
                return(1.0*d/f1)
            if f2==(f1-d) and e2==2:
                return(1.0*(f1-d)/f1)
            return(0)
        else:
            return(0)


def policyEval(v,pi,R):
    gamma = 1
    v_next = np.zeros(v.shape)

    for s in range(len(v_next)):
        v_sum = sum( [ pi[s][a]*(R[s][a] + gamma*sum([Pmat(a,s,s2)*v[s2] for s2 in range(len(v))])) for a in range(pi.shape[1])] )
        v_next[s] = v_sum

    return(v_next)


def policyImprove(v,pi,R):
    pi_new = np.zeros(pi.shape)

    for s in range(len(v)):
        q_list = [sum( [R[s][a]] + [Pmat(a,s,s2)*v[s2] for s2 in range(len(v))]) for a in range(pi.shape[1])]
        best_a = np.argmax(q_list)
        pi_new[s][best_a] = 1.0

    return(pi_new)


R_sa = np.ones((2*N+1,N+1))*-900

#solved state
R_sa[0,:] = 0

#1e states are only rewarded for going to the solved state
R_sa[1:N+1,0] = -np.array(list(range(N)))

#2e states can go anywhere except the solved state, and they pay -1 for the drop.
#There are a lot of transitions that might not be legal, but they should be enforced by pmat.
#R_sa[N+1:,1:] = -1
for i in range(1,N+1):
    R_sa[N+i,1:i+1] = -1

Pi_sa = np.zeros((2*N+1,N+1))
v = np.zeros(2*N+1)

print('R:\n',R_sa)

v_log = np.array([v])

for i in range(25):
    print(i)
    v = policyEval(v,Pi_sa,R_sa)
    v_log = np.concatenate((v_log,[v]))
    Pi_sa = policyImprove(v,Pi_sa,R_sa)


print('Pi:\n',Pi_sa)
print('v:',v)

best_moves = np.argmax(Pi_sa,axis=1)
best_moves_2e = best_moves[N+1:]

print('argmax of Pi:',best_moves)
print('best moves for 2 eggs:',best_moves_2e)

#exit(0)

date_string = datetime.now().strftime("%H-%M-%S")
floors_left = np.arange(1,N+1)
plt.plot(floors_left,best_moves_2e,label='best_moves')
plt.plot(floors_left,np.sqrt(floors_left),label='sqrt(f)')
plt.xlabel('f')
plt.legend()
plt.savefig('eggdrop_MDP_{}floor_bestmoves_{}.png'.format(N,date_string))
plt.show()

for i in range(N+1,2*N+1):
    plt.plot(v_log[:,i])

plt.xlabel('iterations')
plt.savefig('eggdrop_MDP_{}floor_v_{}.png'.format(N,date_string))
plt.show()


#
