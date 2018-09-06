import numpy as np
from random import randint,random
import matplotlib.pyplot as plt

class EggdropAgent:


    def __init__(self,egg_env):

        #Not great, but right now s in the actual index in pi, Q, E, etc,
        #whereas a is the FLOOR NUMBER, so index 0 corresponds to a=1, and
        #I pass the actual floor number to the action function...
        np.set_printoptions(precision=2)
        self.lambda_lookahead = 0.1
        self.gamma = 0.9
        self.alpha = .9
        self.eps = 0.5
        self.env = egg_env
        self.N_floors = self.env.N_floors

        #Needs to be N_s x N_a
        self.pi = np.ones((2+2*self.N_floors,self.N_floors))*(1.0/self.N_floors)
        self.Q = np.zeros((2+2*self.N_floors,self.N_floors))
        #print('size of pi, E, Q:',self.pi.size)
        #print(self.pi)


    def resetE(self):
        self.E = np.zeros((2+2*self.N_floors,self.N_floors))


    def getStartingState(self):
        #return(1 + 2*self.N_floors)
        return(randint(2 + self.N_floors,1 + 2*self.N_floors))


    def getFloorsAndEggsRemainingFromState(self):
        if self.s==0 or self.s==1:
            #print('in terminal state %d' % self.s)
            return((0,0))

        if self.s>=2 and self.s<=(1+self.N_floors):
            #We do this, not s-2, because I want it so s=2 is floor 1, not floor 0.
            e = 1
            f = self.s-1
            return((e,f))

        if self.s>(1+self.N_floors) and self.s<=(1+2*self.N_floors):
            e = 2
            f = self.s-1-self.N_floors
            return((e,f))


    def getRandomAction(self):
        return(randint(1,self.getFloorsAndEggsRemainingFromState()[1]))


    def getEpsGreedyAction(self,state):

        actions = self.Q[state,:]
        best_index = np.argmax(actions)

        if random()>=self.eps:
            #means we're taking the argmax. Do +1 because we want floor #, not index...ugh
            return(best_index+1)
        else:
            return(randint(1,len(actions)))

    def updateQ(self):
        #This does a backwards view update of Q.
        #self.Q += self.alpha*np.multiply(self.TDerror(),self.E)
        self.Q += self.alpha*self.TDerror()*self.E

    #I think only TDerror and the incrementE functions access elements directly, so I should only have to
    #adjust the indices of a for them.
    def TDerror(self):
        return(self.R + self.gamma*self.Q[self.s_next,self.a_next-1] - self.Q[self.s,self.a-1])

    def incrementCurStateActionE(self):
        self.E[self.s,self.a-1] += 1

    def decayE(self):
        self.E = self.gamma*self.lambda_lookahead*self.E



    def learnEpisode(self):

        self.R_tot = 0

        #This will run one full episode with the environment, learning at each time step.
        self.time_step = 0
        self.state_history = []
        self.action_history = []




        #Reset the eligibility trace matrix
        self.resetE()


        '''print('start Q:')
        print(self.Q)

        print('start E:')
        print(self.E)'''

        #Get the starting state (N floors, 2e) and put it in the history array.
        self.s = self.getStartingState()

        #Generate the episode
        self.env.generateEpisode(self.getFloorsAndEggsRemainingFromState()[1])

        '''print()
        print(self.s)'''
        self.state_history.append(self.s)
        #We have to do one SAR cycle to be able to update Q's.
        self.a = self.getEpsGreedyAction(self.s)
        #print('dropping from randomly chosen floor',self.a)
        self.action_history.append(self.a)
        #Run forever unless we manually stop it.


        '''print('\naction hist', self.action_history)
        print('state hist', self.state_history)'''

        while True:

            if self.s==0:
                #print('in solved state, exiting!')
                return((0,self.R_tot))
                break
            if self.s==1:
                #print('in both eggs broken state, exiting!')
                return((1,self.R_tot))
                break

            #So above this line, you have the SA from SARS'A'.
            (self.R,self.s_next) = self.env.performAction(self.s,self.a)
            #print('\n\nperformed action {}, got reward {} and next state {}'.format(self.a,self.R,self.s_next))
            self.R_tot += self.R
            #print('got reward {} and next state {} ({} eggs, floor {})'.format(self.R,self.s,self.getFloorsAndEggsRemainingFromState()[0],self.getFloorsAndEggsRemainingFromState()[1]))

            '''print('\naction hist', self.action_history)
            print('state hist', self.state_history)'''

            #print('dropping from randomly chosen floor',self.a)
            self.a_next = self.getEpsGreedyAction(self.s_next)
            #self.a_next = self.getRandomAction()

            #print('got next e-greedy action',self.a_next)

            #Increment E and update Q, and then decay E
            #print('incrementing E, updating Q, decaying E')
            self.incrementCurStateActionE()
            self.updateQ()
            self.decayE()

            '''print('updated Q:')
            print(self.Q)
            print('updated E:')
            print(self.E)'''

            #updating s and a
            (self.s,self.a) = (self.s_next,self.a_next)
            self.state_history.append(self.s)
            self.action_history.append(self.a)


            #increment the time step
            self.time_step += 1


        #print('\n\n')
        '''print(self.Q)
        exit(0)'''



    def runManyEpisodes(self,N_eps):

        Rs = []
        results = []
        eps = []
        eps.append(self.eps)

        for i in range(1,N_eps):

            (result,R) = self.learnEpisode()
            '''print('\naction hist', self.action_history)
            print('state hist', self.state_history)'''
            #self.eps *= .99
            #self.alpha = 1.0/float(i)

            self.eps *= .999
            eps.append(self.eps)
            Rs.append(R)
            results.append(result)

        print('\n\nending Q:\n\n')
        print(self.Q)

        fig, axes = plt.subplots(3,3,figsize=(14,10))

        axes[0,0].plot(Rs,label='R')
        axes[0,0].legend()

        axes[1,0].plot(results,label='results')
        axes[1,0].legend()

        axes[2,0].plot(eps,label='eps')
        axes[2,0].legend()


        for i in range(2,self.N_floors-5):
            axes[0,1].plot(self.Q[i,:],label='1e,f={}'.format(i-1))

        axes[0,1].set_xlabel('action index')
        axes[0,1].legend()


        for i in range(1+self.N_floors+6,1+2*self.N_floors):
            axes[1,1].plot(self.Q[i,:],label='2e,f={}'.format(i-self.N_floors))

        axes[1,1].set_xlabel('action index')
        axes[1,1].legend()


        axes[0,2].plot(np.argmax(self.Q[2:2+self.N_floors,:],axis=1),label='Q{}'.format('a'))
        axes[0,2].set_xlabel('state index for 1e')
        axes[0,2].set_ylabel('argmax for state')
        axes[0,2].legend()

        axes[1,2].plot(np.argmax(self.Q[2+self.N_floors:,:],axis=1),label='Q{}'.format('a'))
        axes[1,2].set_xlabel('state index for 2e (0 is 1f)')
        axes[1,2].set_ylabel('argmax for state')
        axes[1,2].legend()
        plt.show()


        exit(0)







#
