import json

access_name = {
    "player_name" : "Nutella_Choco",
    "ID" : "8d3s-83k5-89s908",
    "inventory" : {
        "Armor" : {
            "helmet" : "Diamond",
            "chest" : "nederite",
            "pants" : "Diamond",
            "shose" : None
        },
        "quick_0" : "Diamond_Pickaxe",
        "quick_1" : None,
    },
    "Level" : 100
}

with open('C:/anaconda3 for study/gitgit/RWL_Intern/docs/md/junhea_workspace/json_study/test.json', 'w') as f:
    json.dump(access_name, f, indent=4)