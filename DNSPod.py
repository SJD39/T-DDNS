# -*- coding: utf-8 -*-
import requests
import hashlib, hmac, json, os, sys, time
from datetime import datetime


def getAuthorization(action, params, timestamp):
    error = ""
    # 密钥参数
    # 需要设置环境变量 TENCENTCLOUD_SECRET_ID，值为示例的 AKIDz8krbsJ5yKBZQpn74WFkmLPx3*******
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    # 需要设置环境变量 TENCENTCLOUD_SECRET_KEY，值为示例的 Gu5t9xGARNpq86cd98joQYCN3*******
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")

    if secret_id == None:
        error = "无法获取secret_id，请检查是否正确设置环境变量"
        return "", error
    if secret_key == None:
        error = "无法获取secret_key，请检查是否正确设置环境变量"
        return "", error

    service = "dnspod"
    host = "dnspod.tencentcloudapi.com"
    endpoint = "https://" + host
    region = "ap-guangzhou"
    # action = "DescribeInstances"
    version = "2021-03-23"
    algorithm = "TC3-HMAC-SHA256"
    # timestamp = int(time.time())
    # timestamp = 1551113065
    date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
    # params = {"Limit": 1, "Filters": [{"Values": [u"未命名"], "Name": "instance-name"}]}

    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    payload = json.dumps(params)
    canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (
        ct,
        host,
        action.lower(),
    )
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (
        http_request_method
        + "\n"
        + canonical_uri
        + "\n"
        + canonical_querystring
        + "\n"
        + canonical_headers
        + "\n"
        + signed_headers
        + "\n"
        + hashed_request_payload
    )
    print(canonical_request)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(
        canonical_request.encode("utf-8")
    ).hexdigest()
    string_to_sign = (
        algorithm
        + "\n"
        + str(timestamp)
        + "\n"
        + credential_scope
        + "\n"
        + hashed_canonical_request
    )
    print(string_to_sign)

    # ************* 步骤 3：计算签名 *************
    # 计算签名摘要函数
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(
        secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    print(signature)

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (
        algorithm
        + " "
        + "Credential="
        + secret_id
        + "/"
        + credential_scope
        + ", "
        + "SignedHeaders="
        + signed_headers
        + ", "
        + "Signature="
        + signature
    )
    print(authorization)

    print(
        "curl -X POST "
        + endpoint
        + ' -H "Authorization: '
        + authorization
        + '"'
        + ' -H "Content-Type: application/json; charset=utf-8"'
        + ' -H "Host: '
        + host
        + '"'
        + ' -H "X-TC-Action: '
        + action
        + '"'
        + ' -H "X-TC-Timestamp: '
        + str(timestamp)
        + '"'
        + ' -H "X-TC-Version: '
        + version
        + '"'
        + ' -H "X-TC-Region: '
        + region
        + '"'
        + " -d '"
        + payload
        + "'"
    )
    return authorization, error


def DescribeRecordList(Domain, Subdomain, RecordType):
    api = "https://dnspod.tencentcloudapi.com"
    timestamp = int(time.time())
    body = {"Domain": Domain, "Subdomain": Subdomain, "RecordType": RecordType}

    authorization, error = getAuthorization("DescribeRecordList", body, timestamp)
    if error != "":
        return "", error

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-TC-Action": "DescribeRecordList",
        "X-TC-Region": "ap-guangzhou",
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": "2021-03-23",
        "Host": "dnspod.tencentcloudapi.com",
        "Authorization": authorization,
    }

    r = requests.post(api, data=json.dumps(body), headers=headers, timeout=10)
    backJson = json.loads(r.text)

    return backJson, error


def CreateRecord(Domain, RecordType, RecordLine, Value, SubDomain="@", TTL=600):
    api = "https://dnspod.tencentcloudapi.com"
    timestamp = int(time.time())

    body = {
        "Domain": Domain,
        "RecordType": RecordType,
        "RecordLine": RecordLine,
        "Value": Value,
        "SubDomain": SubDomain,
        "TTL": TTL,
    }

    authorization, error = getAuthorization("CreateRecord", body, timestamp)
    if error != "":
        return "", error

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-TC-Action": "CreateRecord",
        "X-TC-Region": "ap-guangzhou",
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": "2021-03-23",
        "Host": "dnspod.tencentcloudapi.com",
        "Authorization": authorization,
    }

    r = requests.post(api, data=json.dumps(body), headers=headers, timeout=10)
    backJson = json.loads(r.text)

    return backJson


def ModifyRecord(
    Domain, RecordType, RecordLine, Value, RecordId, SubDomain="@", TTL=600
):
    api = "https://dnspod.tencentcloudapi.com"
    timestamp = int(time.time())
    body = {
        "Domain": Domain,
        "RecordType": RecordType,
        "RecordLine": RecordLine,
        "RecordId": RecordId,
        "Value": Value,
        "SubDomain": SubDomain,
        "TTL": TTL,
    }

    authorization, error = getAuthorization("ModifyRecord", body, timestamp)
    if error != "":
        return "", error

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-TC-Action": "ModifyRecord",
        "X-TC-Region": "ap-guangzhou",
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": "2021-03-23",
        "Host": "dnspod.tencentcloudapi.com",
        "Authorization": authorization,
    }

    r = requests.post(api, data=json.dumps(body), headers=headers, timeout=10)
    backJson = json.loads(r.text)

    return backJson


def ModifyRecordFields(Domain, RecordId, FieldList):
    api = "https://dnspod.tencentcloudapi.com"
    timestamp = int(time.time())
    body = {"Domain": Domain, "RecordId": RecordId, "FieldList": FieldList}

    authorization, error = getAuthorization("ModifyRecordFields", body, timestamp)
    if error != "":
        return "", error

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-TC-Action": "ModifyRecordFields",
        "X-TC-Region": "ap-guangzhou",
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": "2021-03-23",
        "Host": "dnspod.tencentcloudapi.com",
        "Authorization": authorization,
    }

    r = requests.post(api, data=json.dumps(body), headers=headers, timeout=10)
    backJson = json.loads(r.text)

    return backJson
