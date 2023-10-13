from MDP import MDP
from tqdm import tqdm
import numpy as np

class ValueIteration(MDP):

    def __init__(self, gamma=0.95, epsilon=10e-10):
        super().__init__()
        self.gamma = gamma
        self.epsilon = epsilon
        self.policy = {}
        self.V = {}

    def _init_V(self):
        for state in self.states:
            self.V[state] = 0
    
    def _init_P(self):
        for state in self.states:
            self.policy[state] = None

    def initialize(self):
        self.generate_states()
        self.generate_actions()
        self.termination_states()
        self._init_V()
        self._init_P()

    def value_iteration(self):
        self.initialize()
        epoch = 0
        while True:
            print(f"Epoch {epoch + 1} started...")
            epoch += 1
            delta = 0
            for s in tqdm(self.states):
                if s in self.T_states:
                    self.V[s] = self.reward_function(s)
                    continue
                v = self.V[s]
                new_value = float("-inf")
                for a in self.actions[s]:
                    for s_prime in self.possible_next_states(s, a):
                        expected_value = self.improved_transition_probability(s, a)* (self.reward_function(s_prime) + self.gamma * self.V[s_prime])
                        #expected_value = self.transition_function(s) * (self.reward_function(s_prime) + self.gamma * self.V[s_prime])
                self.V[s] = max(new_value, expected_value)
                delta = max(delta, abs(v - self.V[s]))
            if delta < self.epsilon:
                break

        for s in self.states:
            if s in self.T_states:
                continue
            best_action = None
            best_value = float("-inf")
            for a in self.actions[s]:
                expected_value = self.reward_function(s)
                for s_prime in self.possible_next_states(s, a):
                    expected_value += self.improved_transition_probability(s, a)* (self.reward_function(s_prime) + self.gamma * self.V[s_prime])
                    #expected_value += self.transition_function(s) * (self.reward_function(s_prime) + self.gamma * self.V[s_prime])
                if expected_value > best_value:
                    best_value = expected_value
                    best_action = a
            self.policy[s] = best_action

class PolicyIteration(MDP):
    def __init__(self, gamma = 0.95, epsilon = 10e-10):
        super().__init__()
        self.gamma = gamma
        self.epsilon = epsilon
        self.policy = {}
        self.V = {}
        self.initialize()

    def initialize(self):
        self.generate_states()
        self.generate_actions()
        self.termination_states()
        # initialize random policy and values with zeros
        for i in self.states:
            # choose random action for each state
            self.policy[i] = np.random.choice(self.actions[i]) if self.actions[i] else None
            self.V[i] = 0

    def policy_evaluation(self):
        while True:
            delta = 0
            for s in self.states:
                if s in self.T_states:
                    self.V[s] = self.reward_function(s)
                    continue
                v = 0
                for s_prime in self.possible_next_states(s, self.policy[s]):
                    v += self.reward_function(s_prime) + self.gamma * self.V[s_prime]
                delta = max(delta, np.abs(v - self.V[s]))
                self.V[s] = v
            if delta < self.epsilon:
                break
    
    def policy_improvement(self):
        for s in self.states:
            temp = self.policy[s]
            if s in self.T_states:
                continue
            best_action = None
            best_value = float("-inf")
            stable = True
            for a in self.actions[s]:
                expected_value = self.reward_function(s)
                for s_prime in self.possible_next_states(s, a):
                    expected_value += self.transition_function(s) * (self.reward_function(s_prime) + self.gamma * self.V[s_prime])
                if expected_value > best_value:
                    best_value = expected_value
                    best_action = a
            self.policy[s] = best_action
            if temp != self.policy[s]:
                stable =  False
        return stable
    
    def policy_iteration(self):
        i = 0
        while True:
            print(f"Epoch {i + 1} started...")
            i += 1
            self.policy_evaluation()
            if self.policy_improvement():
                break
        return self.policy