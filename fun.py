import requests


def getIpv6():
    error = ""
    api = "http://6.ipw.cn/"
    try:
        r = requests.get(api)
        ip = r.text
    except:
        error = "访问6.ipw.cn错误"
        return '', error
    return ip, error
