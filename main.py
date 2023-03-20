import fun
import time
import DNSPod
import config

while(True):
    time.sleep(10)
    print("check")
    configJson = config.readConfig()

    # 循环检查记录和配置值是否一致
    for record in configJson:
        print(record)
        # 获取记录列表
        DescribeRecordList = DNSPod.DescribeRecordList(record['Domain'], record['SubDomain'])
        print(DescribeRecordList)

        if "Error" in DescribeRecordList['Response']:
            if DescribeRecordList['Response']['Error']['Code'] == "ResourceNotFound.NoDataOfRecord":
                # 如果没有记录
                # 添加记录
                CreateRecord = DNSPod.CreateRecord(
                    record['Domain'], 
                    record['RecordType'], 
                    record['RecordLine'], 
                    fun.getIpv6(), 
                    SubDomain=record['SubDomain'], 
                    TTL=record['TTL']
                )
                print(CreateRecord)
        