import numpy as np
from random import randint,random
import matplotlib.pyplot as plt

class EggdropAgent:


    def __init__(self,egg_env,lambda_lookahead = 0.9,gamma = 0.9,alpha = .9,eps = 0.05,eps_decay=0.999):

        #Not great, but right now s in the actual index in pi, Q, E, etc,
        #whereas a is the FLOOR NUMBER, so index 0 corresponds to a=1, and
        #I pass the actual floor number to the action function...
        np.set_printoptions(precision=2,linewidth=150)
        self.lambda_lookahead = lambda_lookahead
        self.gamma = gamma
        self.alpha = alpha #0.3, 0.1 seems promising
        self.eps = eps
        self.env = egg_env
        self.N_floors = self.env.N_floors
        self.eps_decay = eps_decay
        #Needs to be N_s x N_a
        #self.Q = (np.zeros((2+2*self.N_floors,self.N_floors))-self.N_floors)
        self.Q = np.zeros((2+2*self.N_floors,self.N_floors))

        self.N_samps = np.zeros((2+2*self.N_floors,self.N_floors))



    def resetE(self):
        self.E = np.zeros((2+2*self.N_floors,self.N_floors))


    def getRandom2eStartingState(self):
        return(randint(2 + self.N_floors,1 + 2*self.N_floors))


    def getTopFloorStartingState(self):
        return(1 + 2*self.N_floors)


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


    def greedyAction(self,state):
        actions = self.Q[state,:]
        best_index = np.argmax(actions)
        return(best_index+1)


    def getAction(self,state):
        #This is just so I only have to comment out one line when switching methods.
        #return(self.greedyAction(state))
        return(self.getEpsGreedyAction(state))

    def updateQ(self):
        #This does a backwards view update of Q.
        #self.Q += self.alpha*np.multiply(self.TDerror(),self.E)
        #self.Q += self.alpha*self.TDerror()*self.E
        self.Q += self.TDerror()*np.multiply(np.sqrt(1.0/(self.N_samps+1.0)),self.E)
        #self.Q += self.TDerror()*np.multiply(1.0/(self.N_samps+1.0),self.E)
        self.updateN()

    def updateN(self):
        #This will make a boolean array with the values of E that are bigger than 0
        #equal 1, so then we can just update N with those.
        self.N_samps[self.s,self.a-1] += 1
        '''updated_elements = (self.E > 0).astype(int)
        self.N_samps += updated_elements'''

    #I think only TDerror and the incrementE functions access elements directly, so I should only have to
    #adjust the indices of a for them.
    def TDerror(self):
        return(self.R + self.gamma*self.Q[self.s_next,self.a_next-1] - self.Q[self.s,self.a-1])

    def incrementCurStateActionE(self):
        self.E[self.s,self.a-1] += 1

    def decayE(self):
        self.E = self.gamma*self.lambda_lookahead*self.E

    def learnEpisode(self,starting_state=None):

        self.R_tot = 0

        #This will run one full episode with the environment, learning at each time step.
        self.time_step = 0
        self.state_history = []

        #Reset the eligibility trace matrix
        self.resetE()

        '''print('start Q:')
        print(self.Q)

        print('start E:')
        print(self.E)'''

        #Get the starting state (N floors, 2e) and put it in the history array.
        if starting_state is None:
            self.s = self.getTopFloorStartingState()
        else:
            self.s = starting_state

        self.state_history.append(self.s)

        self.a = self.getAction(self.s)

        #Generate the episode
        self.env.generateEpisode(self.getFloorsAndEggsRemainingFromState()[1])

        '''print()
        print(self.s)'''

        #print('dropping from randomly chosen floor',self.a)
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
            #self.a_next = self.getEpsGreedyAction(self.s_next)
            self.a_next = self.getAction(self.s_next)
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


            #increment the time step
            self.time_step += 1


        #print('\n\n')
        '''print(self.Q)
        exit(0)'''



    def runManyEpisodes(self,N_eps,starting_state_list=None,starting_action_list=None,show_plot=True,savefig=False):

        Rs = []
        results = []
        eps = []
        eps.append(self.eps)

        if starting_state_list is None:
            print('running {} episodes'.format(N_eps))
            for i in range(1,N_eps):

                if i%int(N_eps/10)==0:
                    print('done with {} episodes'.format(i))

                (result,R) = self.learnEpisode()
                '''print('\naction hist', self.action_history)
                print('state hist', self.state_history)'''
                #self.eps *= .99
                #self.alpha = 1.0/float(i)
                self.eps *= self.eps_decay
                eps.append(self.eps)
                Rs.append(R)
                results.append(result)
        else:
            print('running {} episodes'.format(len(starting_state_list)))
            for i,ss in enumerate(starting_state_list):
                if i%int(len(starting_state_list)/10)==0:
                    print('done with {} episodes'.format(i))

                (result,R) = self.learnEpisode(starting_state=ss)
                '''print('\naction hist', self.action_history)
                print('state hist', self.state_history)'''
                #self.eps *= .99
                #self.alpha = 1.0/float(i)
                eps.append(self.eps)
                Rs.append(R)
                results.append(result)


        print('\n\nending Q:\n\n')
        print(self.Q)

        fig, axes = plt.subplots(3,3,figsize=(14,10))

        ax_eps = None
        ax_res = None

        ax_R = axes[0,0]
        #ax_res = axes[1,0]
        ax_Nsum = axes[1,0]
        ax_eps = axes[2,0]

        ax_Q_1e = axes[0,1]
        ax_argmax_1e = axes[1,1]
        #ax_argmax_vals_1e = axes[2,1]


        ax_Q_2e = axes[0,2]
        ax_argmax_2e = axes[1,2]
        #ax_argmax_vals_2e = axes[2,2]

        if ax_R is not None:
            ax_R.plot(Rs,label='R')
            ax_R.legend()

        if ax_res is not None:
            ax_res.plot(results,label='results')
            ax_res.legend()

        if ax_eps is not None:
            ax_eps.plot(eps,label='eps')
            ax_eps.legend()

        if ax_Nsum is not None:
            ax_Nsum.plot(np.sum(self.N_samps,axis=1),label='Nsum')
            ax_Nsum.set_xlabel('state')
            ax_Nsum.legend()


        for i in range(2,self.N_floors-5):
            ax_Q_1e.plot(self.Q[i,:],label='1e,f={}'.format(i-1))

        ax_Q_1e.set_xlabel('action index')
        #ax_Q_1e.legend()


        for i in range(1+self.N_floors+6,1+2*self.N_floors):
            ax_Q_2e.plot(self.Q[i,:],label='2e,f={}'.format(i-self.N_floors))

        ax_Q_2e.set_xlabel('action index')
        #ax_Q_2e.legend()


        ax_argmax_1e.plot(np.argmax(self.Q[2:2+self.N_floors,:],axis=1),label='Q{}'.format('a'))
        ax_argmax_1e.set_xlabel('state index for 1e')
        ax_argmax_1e.set_ylabel('argmax for state')
        #ax_argmax_1e.legend()

        ax_argmax_2e.plot(np.sqrt(np.arange(0,self.N_floors,1)),'r-',linestyle='dashed')
        ax_argmax_2e.plot(np.argmax(self.Q[2+self.N_floors:,:],axis=1),label='Q{}'.format('a'))
        ax_argmax_2e.set_xlabel('state index for 2e (0 is 1f)')
        ax_argmax_2e.set_ylabel('argmax for state')
        #ax_argmax_2e.legend()

        plt.tight_layout()

        if savefig:
            fname = '{}f_alpha{}_gamma{}_lambda{}_whole.png'.format(self.N_floors,self.alpha,self.gamma,self.lambda_lookahead)
            fig.savefig(fname)

            fname = '{}f_1e_alpha{}_gamma{}_lambda{}.png'.format(self.N_floors,self.alpha,self.gamma,self.lambda_lookahead)
            extent = ax_argmax_1e.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            # Pad the saved area by 10% in the x-direction and 20% in the y-direction
            fig.savefig(fname, bbox_inches=extent.expanded(1.2, 1.2))

            fname = '{}f_2e_alpha{}_gamma{}_lambda{}.png'.format(self.N_floors,self.alpha,self.gamma,self.lambda_lookahead)
            extent = ax_argmax_2e.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            # Pad the saved area by 10% in the x-direction and 20% in the y-direction
            fig.savefig(fname, bbox_inches=extent.expanded(1.2, 1.2))

        if show_plot:
            plt.show()



    def inspectState(self,N_eps,state):


        if state < 2 + self.N_floors:
            print('state in wrong range:',state)
            exit(0)

        f = state - (self.N_floors+1)
        fig, axes = plt.subplots(1,2,figsize=(18,8))

        #One array for each action of this Q(s,*)
        Q_history = np.expand_dims(self.Q[state,:],axis=1)


        for i in range(1,N_eps):
            (result,R) = self.learnEpisode(starting_state=state)
            Q_history = np.concatenate((Q_history,np.expand_dims(self.Q[state,:],axis=1)),axis=1)


        ax_Qsa = axes[0]
        for i,Q_action_history in enumerate(Q_history):

            ax_Qsa.plot(Q_action_history,label='a={}'.format(i))

        ax_Qsa.legend()
        ax_Qsa.set_title('argmax of Q({},*): a={}'.format(f,self.greedyAction(state)-1))




        plt.show()


    def plot_misc(self):

        plt.close('all')
        #plt.clf()
        fig,ax = plt.subplots(1,2,figsize=(18,8))
        #fig,ax = plt.subplots(1,1)
        print(ax.shape)
        #exit(0)

        ax_N = ax[0]
        ax_Q = ax[1]

        Nmat = ax_N.matshow(self.N_samps,cmap='Reds')

        for s in range(self.N_samps.shape[0]):
            ax_N.plot(np.argmax(self.N_samps[s,:]),s,'bo',markersize=3)

        ax_N.set_title('N samps')
        ax_N.set_xlabel('a')
        ax_N.set_ylabel('s')
        fig.colorbar(Nmat,ax=ax_N)

        print('Q[:,0]:')
        print(self.Q[:,0])

        Qmat = ax_Q.matshow(self.Q,cmap='Blues')

        for s in range(self.Q.shape[0]):
            ax_Q.plot(np.argmax(self.Q[s,:]),s,'ro',markersize=3)

        ax_Q.set_title('Q')
        ax_Q.set_xlabel('a')
        ax_Q.set_ylabel('s')
        fig.colorbar(Qmat,ax=ax_Q)


        plt.show()

        exit(0)




#
