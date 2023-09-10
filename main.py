import fun
import time
import DNSPod
import configFile

def main():
    print("开始检查")

    # 获取ip地址
    ip,error = fun.getIpv6()
    if error != '':
        print(error)
        return
    
    # 获取配置文件
    config = configFile.readConfig()
    print(config)
    
    # 循环配置记录
    for configRecord in config:
        print(configRecord)

        # 获取记录列表
        DescribeRecordList,error = DNSPod.DescribeRecordList(configRecord['Domain'], configRecord['SubDomain'], configRecord['RecordType'])
        if error != '':
            print(error)
            return

        # 处理获取列表错误
        if "Error" in DescribeRecordList['Response']:
            if DescribeRecordList['Response']['Error']['Code'] == "ResourceNotFound.NoDataOfRecord":
                # 如果没有记录
                # 添加记录
                CreateRecord = DNSPod.CreateRecord(
                    configRecord['Domain'], 
                    configRecord['RecordType'], 
                    configRecord['RecordLine'], 
                    ip, 
                    SubDomain=configRecord['SubDomain'], 
                    TTL=configRecord['TTL']
                )
                print(CreateRecord)
                continue
        
        # 判断记录值是否和本机ip一致
        if DescribeRecordList['Response']['RecordList'][0]['Value'] == ip:
            continue

        # 修改记录
        ModifyRecordFields = DNSPod.ModifyRecordFields(
            configRecord['Domain'],
            DescribeRecordList['Response']['RecordList'][0]['RecordId'],
            [
                {
                    "Key": "value",
                    "Value": str(ip)
                }
            ]
        )
        print(ModifyRecordFields)
    
while(True):
    time.sleep(10)
    main()