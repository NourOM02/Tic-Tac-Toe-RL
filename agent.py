from TicTacToe import TicTacToe
import numpy as np


# generate all possible moves

def generate_states():
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

def impossible_states():
    states = generate_states()
    # remove states where X or O are superior than 5
    for state in states.copy():
        if abs(state.count(1) - state.count(2)) > 1:
            states.remove(state)
        elif check_2_win(state):
            states.remove(state)
    return states

def check_2_win(state):
    count_h, count_v = 0, 0
    for i in range(3):
        if state[i*3] == state[i*3+1] == state[i*3+2] and (state[i] != 0):
            count_h += 1
        if state[i] == state[3+i] == state[6+i] and (state[i] != 0):
            count_v += 1
    if count_h == 2 or count_v == 2:
        return True
    return False

def rotate_state(state):
    # generate all possible rotation
    new_states = []
    rot = {0:2, 1:5, 2:8, 3:1, 4:4, 5:7, 6:0, 7:3, 8:6}
    for _ in range(3):
        new_state = []
        for i in range(9):
            new_state.append(state[rot[i]])
        state = tuple(new_state)
        new_states.append(tuple(new_state))
    return new_states

def rotate_states():
    states = impossible_states()
    new_states = set()
    for state_i in states:
        add = True
        if state_i not in new_states:
            for state_j in rotate_state(state_i):
                if state_j in new_states:
                    add = False
        if add:
            new_states.add(state_i)
    
    return new_states

def generate_actions(states):
    actions = {}
    for state in states:
        actions[state] = []
        if state.count(0) != 0:
            for i in range(9):
                if state[i] == 0:
                    actions[state].append(i)
    return actions

def reward(state, action):
    # defensive move : positive reward

    # offensive move : positive reward

    # useless move : negative reward

    # first 2 moves : indifferent reward
    pass







#################################### TEST #######################################

states = rotate_states()
actions = generate_actions(states)

state = ()
while state not in states:
    state = tuple([np.random.randint(0,3) for _ in range(9)])

print(state)
print(actions[state])