from TicTacToe import TicTacToe
from agent import Agent
import json
from tqdm import tqdm

agent = Agent()
_, Pi = agent.value_iteration()

policy = {}
for x in tqdm(Pi):
    policy[str(x)] = Pi[x]

with open("policy.json", 'w') as json_file:
    json.dump(policy, json_file)