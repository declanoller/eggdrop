import numpy as np
from random import randint


class EggdropEnvironment:


    def __init__(self,N_floors):

        print('\ncreating egg drop environment with %d floors!\n\n' % N_floors)
        self.N_floors = N_floors
        pass

    def generateEpisode(self,N_floors):
        #This one will totally empirically generate an episode.
        #It will choose a break floor, b, and then let you drop and just check
        #if it breaks or not.

        #I think we'll update break floor by subtracting stuff so it's
        #relevant to the subproblem.
        self.break_floor = randint(1,N_floors)

        #print('\n\nbreak floor for this episode is: {}'.format(self.break_floor))

    def performAction(self,s,a_drop):
        #Here you give it the floor you want to drop on. You return the reward
        #and the new state it's in.

        #s=0 is the solved terminal state and s=1 is the both eggs broken terminal state,
        #so that should be handled outside of this function, so we should never get here.
        if s==0 or s==1:
            print('problem already done, shouldnt be here')
            exit(0)

        #If s isn't one of the special terminal cases, define e and f.
        if s>=2 and s<=(1+self.N_floors):
            e = 1
            #We do this, not s-2, because I want it so s=2 is floor 1, not floor 0.
            f = s-1

        if s>(1+self.N_floors) and s<=(1+2*self.N_floors):
            e = 2
            f = s-1-self.N_floors


        #You can't really run this with break floor > f, because then if you
        #try and do some a < break floor AND a > f, it won't break, so
        #you'll get s_next < 0, which is bad. Usually this shouldn't be a problem
        #because you'll have bf <= f, so even if a>f (a valid but bad move),
        #, you'll have a>=bf, so it will go into that conditional.
        if self.break_floor > f:
            print('invalid scenario, self.break_floor > f')
            print('s',s)
            print('e',e)
            print('f',f)
            print('a',a_drop)
            print('bf',self.break_floor)
            exit(0)

        #This is the special case where I'm gonna say it's solved it: where
        #the break floor is 1 and you also dropped it at 1. It doesn't matter if you
        #have 1 or 2e.

        if self.break_floor==1 and a_drop==1:
            if f==1:
                #print('only 1f remaining, drop doesnt count, R=0')
                R = 0
            if f>1:
                #print('dropped from 1 with bf 1, solved!')
                R = -1
            #R = 100
            s_next = 0
            return((R,s_next))

        #If you drop it above the bf and it breaks.
        if a_drop>=self.break_floor:
            #print('dropped from floor {} out of {}, broke!'.format(a_drop,f))
            if e==1:
                #I think here we need to make it really bad to end with no eggs...
                R = -30
                #Go to the both broken state, return.
                s_next = 1
                return((R,s_next))

            if e==2:
                #So I'm gonna try and define it so that it's not necessarily bad
                #to break an egg, it just costs a drop and probably means you'll
                #get a generally worse result.
                #Question: should you enforce that it goes to subproblem (in this case,
                #it's now only up to floors a_drop) manually, or let it figure it out?
                #For now I'll do it manually, but experiment in the future.
                R = -1
                #It just goes to the floor a_drop (because you know if you dropped it
                #on floor 15/20, you only have to search up to 15 now) with 1e
                s_next = 1 + a_drop
                #You don't have to update the break floor here.
                return((R,s_next))

        #If the drop is below the break floor.
        else:
            #print('dropped from floor {} out of {}, didnt break!'.format(a_drop,f))
            R = -1
            #Need to update the break_floor to reflect the new subproblem
            self.break_floor = self.break_floor - a_drop
            #print('break floor is now %d' % self.break_floor)

            if e==1:
                #Go to the state where you know it can't be broken from.
                s_next = 1 + (f - a_drop)
                return((R,s_next))

            if e==2:
                s_next = 1 + self.N_floors + (f - a_drop)
                return((R,s_next))








#
