import fun
import time
import DNSPod
import configFile

while(True):
    time.sleep(10)
    print("开始检查")
    ipv6 = fun.getIpv6()
    config = configFile.readConfig()

    # 循环配置记录
    for configRecord in config:
        print(configRecord)

        # 获取记录列表
        DescribeRecordList = DNSPod.DescribeRecordList(configRecord['Domain'], configRecord['SubDomain'], configRecord['RecordType'])
        print(DescribeRecordList)

        # 处理获取列表错误
        if "Error" in DescribeRecordList['Response']:
            if DescribeRecordList['Response']['Error']['Code'] == "ResourceNotFound.NoDataOfRecord":
                # 如果没有记录
                # 添加记录
                CreateRecord = DNSPod.CreateRecord(
                    configRecord['Domain'], 
                    configRecord['RecordType'], 
                    configRecord['RecordLine'], 
                    fun.getIpv6(), 
                    SubDomain=configRecord['SubDomain'], 
                    TTL=configRecord['TTL']
                )
                print(CreateRecord)
                continue
        
        # 判断记录值是否和本机ip一致
        if DescribeRecordList['Response']['RecordList'][0]['Value'] == ipv6:
            continue

        # 修改记录
        ModifyRecordFields = DNSPod.ModifyRecordFields(
            configRecord['Domain'],
            DescribeRecordList['Response']['RecordList'][0]['RecordId'],
            [
                {
                    "Key": "value",
                    "Value": str(fun.getIpv6())
                }
            ]
        )
        print(ModifyRecordFields)