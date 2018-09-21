from EggdropEnvironment import EggdropEnvironment
from EggdropAgent import EggdropAgent
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, stdev




f = 25
env = EggdropEnvironment(f)



agent = EggdropAgent(env,gamma=1.0,lambda_lookahead=0.0,alpha=1.1,eps=0.0,note='noavg_randomdrop2e')
agent.runManyEpisodes(2000,savefig=True,show_plot=True)

exit(0)
agent.inspectState(1000,f+22)
agent.inspectState(10000,f+22)




#######################Trying different avging methods

#alphas = np.linspace(0,1.4,30)[1:]
avg_errors = []
SD_errors = []
Ns = [2000,20000,200000]
for N in Ns:
    print(N)
    runs = 5
    err = []
    for run in range(runs):
        agent = EggdropAgent(env,gamma=1.0,lambda_lookahead=0.0,alpha=0.9,eps=0.0,note='trueavg_randomdrop2e')
        agent.runManyEpisodes(N,savefig=False,show_plot=False)
        err.append(agent.theoryError())
    avg_errors.append(mean(err))
    SD_errors.append(stdev(err))


plt.errorbar(list(range(len(Ns))),avg_errors,yerr=SD_errors,fmt='ro-')
plt.xlabel('N_episodes')
plt.ylabel('MSE')
plt.xticks(list(range(len(Ns))),[str(N) for N in Ns])
plt.title('true avg decreasing rate , 25f')
plt.savefig('true_avg_MSE.png')
print('avg errors:',avg_errors)
print('SD errors:',SD_errors)

plt.show()

exit(0)





####################Varying alpha

alphas = np.linspace(0,1.4,30)[1:]
avg_errors = []
SD_errors = []
N = 200000
for a in alphas:
    print(a)
    runs = 5
    err = []
    for run in range(runs):
        agent = EggdropAgent(env,gamma=1.0,lambda_lookahead=0.0,alpha=a,eps=0.0,note='noavg_randomdrop2e')
        agent.runManyEpisodes(N,savefig=False,show_plot=False)
        err.append(agent.theoryError())
    avg_errors.append(mean(err))
    SD_errors.append(stdev(err))


plt.errorbar(alphas,avg_errors,yerr=SD_errors,fmt='ro-')
plt.xlabel('alpha')
plt.ylabel('MSE')
plt.title(str(N)+' episodes, 25f')
plt.savefig(str(N)+'eps_' + 'MSE_vs_alpha.png')
plt.show()
exit(0)

#######################plain ol many episodes runs

agent = EggdropAgent(env,gamma=1.0,lambda_lookahead=0.0,alpha=.05,eps=0.0,note='trueavg_randomdrop2e')
agent.runManyEpisodes(2000000,savefig=True,show_plot=True)

#agent.inspectState(100000,f+22)

exit(0)

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
