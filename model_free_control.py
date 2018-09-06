from EggdropEnvironment import EggdropEnvironment
from EggdropAgent import EggdropAgent




env = EggdropEnvironment(10)

agent = EggdropAgent(env)

#agent.learnEpisode()

agent.runManyEpisodes(200000)














#
