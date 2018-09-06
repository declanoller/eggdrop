import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def v1egg(f):
    return(f-1)

#This is for floors 0 and 1, the anchor cases.
v2egg = [0,0]
best_d = [0,1]

f_limit = 1000

for f in range(2,f_limit+1):

    vd = [1 + (d*1.0/f)*v1egg(d) + ((1.0*f-d)/f)*v2egg[f-d] for d in range(1,f+1)]

    min_d = min(vd)
    best_d_ind = np.argmin(vd)

    best_d.append(best_d_ind + 1)
    v2egg.append(min_d)


print('best for f = {}: avg={}, best move={}'.format(f_limit,v2egg[f_limit],best_d[f_limit]))
print('best d', best_d[:20])

plt.xlabel('f')
plt.ylabel('v(f), best d')
plt.plot(best_d,label='best_d')
plt.plot(v2egg,label='v(f)')
x = np.arange(1,f)
plt.plot(x,np.sqrt(x),label='sqrt(f)',color='darkred')
plt.legend()

date_string = datetime.now().strftime("%H-%M-%S")
plt.savefig('eggdrop_DP_{}floor_{}.png'.format(f_limit,date_string))
plt.show()











#
