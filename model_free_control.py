from EggdropEnvironment import EggdropEnvironment
from EggdropAgent import EggdropAgent
import numpy as np


f = 25
env = EggdropEnvironment(f)




#agent.learnEpisode()

'''agent = EggdropAgent(env,gamma=.99,lambda_lookahead=0.0,alpha=.99,eps=0.0)
agent.runManyEpisodes(20000,savefig=False,show_plot=True)


agent.plot_misc()

exit(0)'''

eps_each = 100
states_ub = 2*f+1
#ss_list = np.concatenate([np.full(eps_each,i) for i in range(2,states_ub+1)])

f_2e_ub = f
f_2e_ub_state = 1+f+f_2e_ub
ss_list = np.concatenate([np.full(eps_each,i) for i in range(2,f_2e_ub_state+1)])


agent = EggdropAgent(env,gamma=.99,lambda_lookahead=0.0,alpha=.99,eps=0.0)
agent.runManyEpisodes(0,starting_state_list=ss_list,savefig=False)

agent.plot_misc()
exit(0)

#Only train the 1e states and some of the 2e states
f_2e_ub = 4
f_2e_ub_state = 1+f+f_2e_ub
ss_list = np.concatenate([np.full(eps_each,i) for i in range(2,f_2e_ub_state+1)])


agent = EggdropAgent(env,gamma=.99,lambda_lookahead=0.99,alpha=.99)
agent.runManyEpisodes(0,starting_state_list=ss_list,savefig=False)

print('Q:')
print(agent.Q[f_2e_ub_state,:])

inspect_f = f_2e_ub_state+1
agent.inspectState(2000,inspect_f)



exit(0)

for g in [.1,.5,.9]:
    for l in [.1,.5,.9]:
        for a in [.1,.5,.9]:
            print('g={},l={},a={}\n'.format(g,l,a))
            agent = EggdropAgent(env,gamma=g,lambda_lookahead=l,alpha=a)
            agent.runManyEpisodes(0,starting_state_list=ss_list,show_plot=False,savefig=True)














#
