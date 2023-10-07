import json

with open("policy.json", 'r') as json_file:
    # open json file as dictionary
    policy = json.load(json_file)
    print(policy["(2, 0, 1, 0, 1, 0, 0, 0, 0)"])