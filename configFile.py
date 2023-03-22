import json

def readConfig():
    configFile = open('./config.json', encoding='utf-8')
    configJson = json.load(configFile)
    configFile.close()
    return configJson
