import numpy as np
from tqdm import tqdm
import random

class Agent:
    def __init__(self, gamma=1.0, epsilon = 0.001) -> None:
        self.gamma = gamma
        self.epsilon = epsilon
    # generate all possible moves
    def _brute_states(self):
        # 0 : no move
        # 1 : X
        # 2 : O
        possible_states = set()
        for a in range(3):
            for b in range(3):
                for c in range(3):
                    for d in range(3):
                        for e in range(3):
                            for f in range(3):
                                for g in range(3):
                                    for h in range(3):
                                        for i in range(3):
                                            possible_states.add((a,b,c,d,e,f,g,h,i))
        return possible_states

    def _check_2_win(self, state):
        count_h, count_v = 0, 0
        for i in range(3):
            if state[i*3] == state[i*3+1] == state[i*3+2] and (state[i] != 0):
                count_h += 1
            if state[i] == state[3+i] == state[6+i] and (state[i] != 0):
                count_v += 1
        if count_h == 2 or count_v == 2:
            return True
        return False
    
    def _check_defense(self, state):
        value = 2 if state.count(1) == state.count(2) else 1
        defenses = set()
        for i in range(3):
            if (state[i*3] == state[i*3+1]) and state[i*3] == value and state[i*3+2] == 0:
                defenses.add(i*3+2)
            elif (state[i*3] == state[i*3+2]) and state[i*3] == value and state[i*3+1] == 0:
                defenses.add(i*3+1)
            elif (state[i*3+1] == state[i*3+2]) and state[i*3+1] == value and state[i*3] == 0:
                defenses.add(i*3)
        for i in range(3):
            if (state[i] == state[3+i]) and state[i] == value and state[6+i] == 0:
                defenses.add(6+i)
            elif (state[i] == state[6+i]) and state[i] == value and state[3+i] == 0:
                defenses.add(3+i)
            elif (state[3+i] == state[6+i]) and state[3+i] == value and state[i] == 0:
                defenses.add(i)
        if state[0] == state[4] and state[0] == value and state[8] == 0:
            defenses.add(8)
        elif state[0] == state[8] and state[0] == value and state[4] == 0:
            defenses.add(4)
        elif state[4] == state[8] and state[4] == value and state[0] == 0:
            defenses.add(0)
        elif state[2] == state[4] and state[2] == value and state[6] == 0:
            defenses.add(6)
        elif state[2] == state[6] and state[2] == value and state[4] == 0:
            defenses.add(4)
        return defenses

    def _check_offense(self, state):
        offenses = set()
        value = 1 if state.count(1) == state.count(2) else 2
        for i in range(3):
            if state[i*3] == value and state[i*3+1] == 0 and state[i*3+2] == 0:
                offenses.add(i*3+1)
                offenses.add(i*3+2)
            elif state[i*3+2] == value and state[i*3+1] == 0 and state[i*3] == 0:
                offenses.add(i*3+1)
                offenses.add(i*3)
            elif state[i*3+1] == value and state[i*3] == 0 and state[i*3+2] == 0:
                offenses.add(i*3)
                offenses.add(i*3+2)
        for i in range(3):
            if state[i] == value and state[i+3] == 0 and state[i+6] == 0:
                offenses.add(i+3)
                offenses.add(i+6)
            elif state[i+6] == value and state[i+3] == 0 and state[i] == 0:
                offenses.add(i+3)
                offenses.add(i)
            elif state[i+3] == value and state[i] == 0 and state[i+6] == 0:
                offenses.add(i)
                offenses.add(i+6)
        if state[0] == value and state[4] == 0 and state[8] == 0:
            offenses.add(4)
            offenses.add(8)
        elif state[8] == value and state[4] == 0 and state[0] == 0:
            offenses.add(4)
            offenses.add(0)
        elif state[4] == value and state[0] == 0 and state[8] == 0:
            offenses.add(0)
            offenses.add(8)
        if state[2] == value and state[4] == 0 and state[6] == 0:
            offenses.add(4)
            offenses.add(6)
        elif state[6] == value and state[4] == 0 and state[2] == 0:
            offenses.add(4)
            offenses.add(2)
        elif state[4] == value and state[2] == 0 and state[6] == 0:
            offenses.add(2)
            offenses.add(6)
        return offenses

    def _check_win(self, state):
        wins = set()
        value = 1 if state.count(1) == state.count(2) else 2
        for i in range(3):
            if state[i*3] == state[i*3+1] and state[i*3+1] == value and state[i*3+2] == 0:
                wins.add(i*3+2)
            elif state[i*3] == state[i*3+2] and state[i*3+2] == value and state[i*3+1] == 0:
                wins.add(i*3+1)
            elif state[i*3+1] == state[i*3+2] and state[i*3+1] == value and state[i*3] == 0:
                wins.add(i*3)
        for i in range(3):
            if state[i] == state[3+i] and state[i] == value and state[6+i] == 0:
                wins.add(6+i)
            elif state[i] == state[6+i] and state[i] == value and state[3+i] == 0:
                wins.add(3+i)
            elif state[3+i] == state[6+i] and state[3+i] == value and state[i] == 0:
                wins.add(i)
        if state[0] == state[4] and state[0] == value and state[8] == 0:
            wins.add(8)
        elif state[0] == state[8] and state[0] == value and state[4] == 0:
            wins.add(4)
        elif state[4] == state[8] and state[4] == value and state[0] == 0:
            wins.add(0)
        elif state[2] == state[4] and state[2] == value and state[6] == 0:
            wins.add(6)
        elif state[2] == state[6] and state[2] == value and state[4] == 0:
            wins.add(4)
        elif state[4] == state[6] and state[4] == value and state[2] == 0:
            wins.add(2)
        return wins
    
    def win(self, state):
        for i in range(3):
            if state[i*3] == state[i*3+1] == state[i*3+2] and state[i*3] != 0:
                return True
            if state[i] == state[3+i] == state[6+i] and state[i] != 0:
                return True
        if state[4] == state[6] == state[2] and state[4] != 0:
            return True
        elif state[0] == state[4] == state[8] and state[0] != 0:
            return True
        else:
            return False

    def states(self):
        states = self._brute_states()
        # remove states where X or O are superior than 5
        for state in states.copy():
            if abs(state.count(1) - state.count(2)) > 1:
                states.remove(state)
            elif self._check_2_win(state):
                states.remove(state)
            elif state.count(2) > state.count(1):
                states.remove(state)
        return states

    def termination_states(self, states):
        T_states = set()
        for state in states:
            if self.win(state):
                T_states.add(state)
            elif state.count(0) == 0:
                T_states.add(state)
        return T_states

    def actions(self, states):
        actions = {}
        for state in states:
            actions[state] = []
            if state.count(0) != 0:
                for i in range(9):
                    if state[i] == 0:
                        actions[state].append(i)
        return actions

    def reward_function(self,state, action):
        defenses = self._check_defense(state)
        offenses = self._check_offense(state)
        wins = self._check_win(state)
        # winning move : maximum reward
        if action in wins:
            return 1000
        # check the defense
        if action in defenses:
            return 10
        # offensive move : positive reward
        if action in offenses:
            return 20
        # useless move : negative reward
        if action not in defenses.union(offenses.union(wins)):
            return -1000
        # first 2 moves : indifferent reward
        if state.count(0) > 7:
            return 0
        
    def transition_function(self, state, actions):
        return 1/len(actions[state])
    
    def value_iteration(self):
        states = self.states()
        T_states = self.termination_states(states)
        actions = self.actions(states)
        
        # Initialize the value function to zeros
        V = {s: 0.0 for s in states}
        epoch = 0
        while True:
            print(f"Epoch {epoch} started...")
            epoch += 1
            delta = 0
            for s in tqdm(states):
                if s in T_states:
                    continue
                v = V[s]
                new_value = float("-inf")

                for a in actions[s]:
                    expected_value = sum(
                        self.transition_function(s, actions) * (self.reward_function(s, a) + self.gamma * V[s_prime])
                        for s_prime in states
                    )
                    new_value = max(new_value, expected_value)

                V[s] = new_value
                delta = max(delta, abs(v - V[s]))
            if delta < self.epsilon:
                break

        # Calculate the optimal policy
        policy = {}

        for s in states:
            # If the game is in a terminal state, there's no action to choose
            if s in T_states:
                policy[s] = None
                continue
            best_action = None
            best_value = float("-inf")
            for a in actions[s]:
                expected_value = self.reward_function(s, a)
                for s_prime in states:
                    expected_value += self.transition_function(s, actions) * (self.gamma * V[s_prime])
                if expected_value > best_value:
                    best_value = expected_value
                    best_action = a
            policy[s] = best_action

        return V, policy