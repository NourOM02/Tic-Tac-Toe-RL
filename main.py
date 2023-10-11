from TicTacToe import TicTacToe
from agents import ValueIteration
import json
from tqdm import tqdm

agent = ValueIteration()
agent.value_iteration()

policy = {}
for x in tqdm(agent.policy):
    policy[str(x)] = agent.policy[x]

with open("policy.json", 'w') as json_file:
    json.dump(policy, json_file)