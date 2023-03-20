import requests

def getIpv6():
    api = "http://6.ipw.cn/"
    r = requests.get(api)
    return r.text