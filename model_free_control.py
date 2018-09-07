from EggdropEnvironment import EggdropEnvironment
from EggdropAgent import EggdropAgent
import numpy as np


f = 10
env = EggdropEnvironment(f)

agent = EggdropAgent(env)

#agent.learnEpisode()

#agent.runManyEpisodes(200000)
eps_each = 100
states_ub = 21
ss_list = np.concatenate([np.full(eps_each,i) for i in range(2,states_ub+1)])
agent.runManyEpisodes(0,starting_state_list=ss_list)














#
