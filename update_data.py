###更新json数据

import json
def update(person,time):
    with open("communicate.json", "r",encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    data["person"] = person
    data["time"]=time
    with open("communicate.json", "w") as jsonFile:
        json.dump(data, jsonFile,ensure_ascii=False)