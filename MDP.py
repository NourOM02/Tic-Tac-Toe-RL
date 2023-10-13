import numpy as np
from tqdm import tqdm
import json

class MDP:
    def __init__(self):
        self.states = set()
        self.T_states = set()
        self.actions = {}
        self.policy = open("Policies/policyIteration.json", "r")
        self.policy = json.load(self.policy)

    def generate_states(self):
        """
        This method generates all possible states of the game
        """

        # define a fucntion to generate all states
        def _brute_states():
            """
            This function generates all possible and impossible states of the game
            """
            # 0 : no move
            # 1 : X
            # 2 : O
            all_board_config = set()
            for a in range(3):
                for b in range(3):
                    for c in range(3):
                        for d in range(3):
                            for e in range(3):
                                for f in range(3):
                                    for g in range(3):
                                        for h in range(3):
                                            for i in range(3):
                                                all_board_config.add((a,b,c,d,e,f,g,h,i))
            return all_board_config
        # define a function to check if there are 2 winners at the same time
        def _check_2_win(state):
            """
            This function checks if there are 2 winners at the same time
            """
            count_h, count_v = 0, 0
            for i in range(3):
                if (state[i*3] == state[i*3+1] == state[i*3+2] and state[i*3] == 1) or (state[i*3] == state[i*3+1] == state[i*3+2] and state[i*3] == 2):
                    count_h += 1
                if (state[i] == state[3+i] == state[6+i] and state[i] == 1) or (state[i] == state[3+i] == state[6+i] and state[i] == 2):
                    count_v += 1
            if count_h == 2 or count_v == 2:
                return True
            return False
        print(_check_2_win((2, 2, 2, 1, 1, 1, 1, 0, 2)))
    
        # initialize states with possible and impossible states
        self.states = _brute_states()
        
        # remove states that are not possible
        for state in self.states.copy():
            # we suppose that computer is always X, thus if there   are more X than O, remove the state
            if state.count(1) > state.count(2):
                self.states.remove(state)
            # if there is a difference between the number of Os and Xs which is superioe to 2, remove the state
            elif abs(state.count(1) - state.count(2)) > 1:
                self.states.remove(state)
            # if there are 2 winners at the same time, remove the state
            elif _check_2_win(state):
                self.states.remove(state)
   
    def termination_states(self):
        """
        This function takes all possible states and updates the states where the game is over wether it is a win, a draw or a loss
        """
        for state in self.states:
            if self.win(state):
                self.T_states.add(state)
            elif state.count(0) == 0:
                self.T_states.add(state)

    # def current_player(self, state):
    #     if self.first_player == 1:
    #         if state.count(1) <= state.count(2):
    #             return 1
    #         else:
    #             return 2
    #     else:
    #         if state.count(1) <= state.count(2):
    #             return 2
    #         else:
    #             return 1

    def generate_actions(self):
        """
        This function takes all possible states and update the possible actions for each state
        """
        for state in self.states:
            self.actions[state] = None
            if state not in self.T_states:
                self.actions[state] = []
                for i in range(9):
                    if state[i] == 0:
                        self.actions[state].append(i)
   
    def transition_function(self, state):
        """
        This function takes a state and returns the probability of each possible next state
        """
        # if the game is over, return 0
        if state in self.T_states:
            return 0
        # if the game is not over, return 1/number of possible actions for O
        else:
            return 1/(len(self.actions[state])-1)
    
    def reward_function(self,state):
        """
        This function takes a state and returns the reward of the state
        """

        if self.win(state) == 1:
            return 10
        if self.win(state) == 2:
            return -10
        return -1
            
    def win(self, state):
        for i in range(3):
            if state[i*3] == state[i*3+1] == state[i*3+2] and state[i*3] != 0:
                return state[i*3]
            if state[i] == state[3+i] == state[6+i] and state[i] != 0:
                return state[i]
        if state[4] == state[6] == state[2] and state[4] != 0:
            return state[4]
        elif state[0] == state[4] == state[8] and state[0] != 0:
            return state[0]
        else:
            return False
    
    def possible_next_states(self, state, action):
        new_state = list(state)
        new_state[action] = 1
        if self.win(new_state):
            return []
        possible_next_states = []
        for i, case in enumerate(new_state):
            next_new_state = new_state.copy()
            if case == 0:
                next_new_state[i] = 2
                possible_next_states.append(tuple(next_new_state))
        
        return possible_next_states
    
    def improved_transition_probability(self, state, action):
        """
        This function takes a state and returns the probability of each possible next state
        inspired from value iteration policy
        """
        # if the game is over, return 0
        if state in self.T_states:
            return 0
        # if the game is not over, return 1/number of possible actions for O
        else:
            return 1 if action == self.policy[state] else 0