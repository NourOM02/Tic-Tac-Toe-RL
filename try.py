import json

with open("policy.json", 'r') as json_file:
    # open json file as dictionary
    policy = json.load(json_file)
    print(policy["(1, 0, 0, 2, 1, 1, 2, 0, 2)"])
