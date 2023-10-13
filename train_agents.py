from agents import ValueIteration, PolicyIteration
import json
from tqdm import tqdm

##################################### Value Iteration #####################################


agent = ValueIteration()
agent.value_iteration()

policy = {}
for x in agent.policy:
    policy[str(x)] = agent.policy[x]

with open("Policies/valueIteration.json", 'w') as json_file:
    json.dump(policy, json_file)


##################################### Policy Iteration #####################################

"""
agent = PolicyIteration()
agent.policy_iteration()

policy = {}
for x in agent.policy:
    policy[str(x)] = agent.policy[x]

with open("Policies/policyIteration.json", 'w') as json_file:
    policy_json = {str(state): int(agent.policy[state]) if agent.policy[state] != None else None for state in agent.policy}
    json.dump(policy_json, json_file)
    """