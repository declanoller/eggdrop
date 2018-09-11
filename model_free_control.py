from EggdropEnvironment import EggdropEnvironment
from EggdropAgent import EggdropAgent
import numpy as np


f = 25
env = EggdropEnvironment(f)




#agent.learnEpisode()

'''agent = EggdropAgent(env,gamma=.99,lambda_lookahead=0.99,alpha=.99)
agent.runManyEpisodes(200000)

exit(0)'''

eps_each = 1000
states_ub = 2*f+1
ss_list = np.concatenate([np.full(eps_each,i) for i in range(2,states_ub+1)])


agent = EggdropAgent(env,gamma=.99,lambda_lookahead=0.99,alpha=.99)
agent.runManyEpisodes(0,starting_state_list=ss_list,savefig=True)

exit(0)

for g in [.1,.5,.9]:
    for l in [.1,.5,.9]:
        for a in [.1,.5,.9]:
            print('g={},l={},a={}\n'.format(g,l,a))
            agent = EggdropAgent(env,gamma=g,lambda_lookahead=l,alpha=a)
            agent.runManyEpisodes(0,starting_state_list=ss_list,show_plot=False,savefig=True)














#
