import json

with open('C:/anaconda3 for study/gitgit/RWL_Intern/docs/md/junhea_workspace/json_study/test.json') as f:
    access_name = json.load(f)

access_name["player_name"] = "TTTTAP"

print(access_name["player_name"])

print(access_name["inventory"])

print(access_name["inventory"]["Armor"]["chest"])

with open('C:/anaconda3 for study/gitgit/RWL_Intern/docs/md/junhea_workspace/json_study/test.json', 'w') as f:
    json.dump(access_name, f, indent=4)