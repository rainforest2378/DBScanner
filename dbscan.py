from flask import Flask
from flask import request
import json
import nmap
import time, datetime
# 创建flask对象
#从数据库读取信息

import pymysql
#import pandas as pd

def ff(s1):
    #s1 = eval(repr(s).replace('\\x', ''))
    print(s1)
    # print(result)
    # print(s.find("2"))
    # s1='0200000401a0400000503abc1300000612information_schema0600000705mysql1300000812performance_schema040000	03sys05'
    a = []
    b = ''
    l = len(s1)
    flag = 0
    for i in range(l):
        if (s1[i].isalpha() or s1[i] == '_') and flag == 1 and s1[i]!='x':
            b = b + s1[i]
        elif (s1[i].isalpha() or s1[i] == '_') and flag == 0  and s1[i]!='x':
            flag = 1
            # count = i
            b = b + s1[i]
        elif s1[i].isdigit() and flag == 1:
            flag = 0
            a.append(b)
            b = ''
        elif s1[i].isdigit() and flag == 0:
            pass
        else:
            pass
    print(a)
    return a
def ff2(s):
    for i in range(len(s)):
        if (s[i].isalpha() or s[i] == '_' or s[i] == '\\' or s[i].isdigit()):
            pass
        else:
            # print(hex((ord(a[i]))))
            a = hex((ord(s[i])))
            a = a.replace('0x', '\\x')
            s = s.replace(s[i], a)
            # print(s)

    print(s)
    s = s.replace('\t', '\\x09')
    s = s.replace('\n', '\\x0A')
    s = s.replace('\r', '\\x0D')
    s=s.replace('%','\\x25')
    print(s)

    a = []
    b = ''
    l = len(s)
    flag1 = 1
    c = 0
    count = 0
    for i in range(l):
        # print(c)
        #print(count)
        # print(s[i])
        if s[i] == '\\':
            c = 1
            if flag1 == 1:
                count = 1
                if b != '':
                    a.append(b)
                b = ''
                flag1 = 0
            else:
                count += 1

        elif s[i] != '\\' and c != 4:
            c += 1
            continue
        elif count == 5 and s[i] != '\\' and c == 4:
            #print(s[i])

            b = b + s[i]
            #print(b)
            flag1 = 1
            continue
        else:
            pass
    print(a)
    return a

# 功能函数
#开始扫描服务信息
def scan(id,service,hostIP,port):
    # result_str = "%s今年%s岁" % (name, age)
    print('----------------------------------------------------')

    print('----------------------------------------------------')
    nm = nmap.PortScanner(nmap_search_path=('nmap',r'D:\Nmap\nmap.exe'))
    user=input("%s : please input user:" %hostIP)
    password=input("%s : please input password:" %hostIP)
    if user == '' or password=='':
        return 0

    a = nm.scan(hosts=hostIP, arguments='--script mysqldatabase --script-args mysqluser=root,mysqlpass=root', ports=port)

    for host in nm.all_hosts():  # 遍历扫描主机
        print(host)

        print('----------------------------------------------------')
        #print('Host : %s (%s)' % (host, nm[host].hostname()))  # 输出主机及主机名
        #print('State : %s' % nm[host].state())  # 输出主机状态，如up、down
        #print(host)
        #hostname = nm[host].hostnames()[0]['name']
        hostip = host
        hoststate = nm[hostIP].state()
        scantime = a['nmap']['scanstats']['timestr']

        for proto in nm[host].all_protocols():  # 遍历扫描协议，如tcp、udp
            # print('----------')
            # print('Protocol : %s' % proto)  # 输入协议名
            protocal = proto
            lport = nm[host][proto].keys()  # 获取协议的所有扫描端口
            sorted(lport)  # 端口列表排序

            for sport in lport:  # 遍历端口及输出端口与状态，服务和版本信息
                portstate = nm[host][proto][sport]['state']
                service = nm[host][proto][sport]['name']
                version = nm[host][proto][sport]['version']
                output=nm[host][proto][sport]['script']
                port = sport
                print('port : %s\t state : %s\t service: %s\t version: %s  output:%s' % (port, portstate, service, version, output))
                #print(output['mysqldatabase2'])
                o=output['mysqldatabase']
                db = ff(o)
                res0=db


                for i in range(len(db)):
                    print(i)
                    print(db[i])
                    argu = '--script mysqldatabase2x --script-args mysqluser=root,mysqlpass=root,db=%s' % db[i]
                    print(argu)
                    a = nm.scan(hosts=host,
                                arguments=argu,
                                ports='3306')

                    for host in nm.all_hosts():  # 遍历扫描主机

                        print('----------------------------------------------------')
                        print('Host : %s (%s)' % (host, nm[host].hostname()))  # 输出主机及主机名
                        print('State : %s' % nm[host].state())  # 输出主机状态，如up、down
                        print(host)
                        hostname = nm[host].hostnames()[0]['name']
                        hostip = host
                        hoststate = nm[host].state()
                        scantime = a['nmap']['scanstats']['timestr']

                        for proto in nm[host].all_protocols():  # 遍历扫描协议，如tcp、udp
                            # print('----------')
                            # print('Protocol : %s' % proto)  # 输入协议名
                            protocal = proto
                            lport = nm[host][proto].keys()  # 获取协议的所有扫描端口
                            sorted(lport)  # 端口列表排序

                            for sport in lport:  # 遍历端口及输出端口与状态，服务和版本信息
                                portstate = nm[host][proto][sport]['state']
                                service = nm[host][proto][sport]['name']
                                version = nm[host][proto][sport]['version']
                                output = nm[host][proto][sport]['script']
                                port = sport
                                print('port : %s\t state : %s\t service: %s\t version: %s  output:%s' % (
                                port, portstate, service, version, output))
                                # print(output['mysqldatabase2'])
                                o = output['mysqldatabase2x']
                                db1 = ff2(o)
                                diction[db[i]]=db1



                                #print(db1)


    #res0 = ','.join(res0)
    #print(res)
                res=diction
                print(res)
                data0='|'.join(res0)

                #data0=json.dumps(res0)
                data = json.dumps(res)
                sql = "insert into DBTables(serviceID,DBNames,tableNames) VALUE (%s,%s,%s)"
                cursor.execute(sql, (id, data0, data))
                conn.commit()



                    #sql = "insert into service_detection(serviceID,DBNames,tableNames) VALUE (%s,%s,%s);"


                    #cursor = conn.cursor()
            #cursor.execute(sql, (serviceID,DBNames,tableNames))
            #conn.commit()






# 连接配置信息
import json

diction={}
#data2 = json.dumps(data)
print('Program now starts on %s')
print('Executing...')

conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                       passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
cursor = conn.cursor()
return_dict=[]
# 执行sql语句

#with conn.cursor() as cursor:
sql = "select * from service_detection"
cursor.execute(sql)
result = cursor.fetchall()
#finally:
#conn.close();
#df = pd.DataFrame(result)  # 转换成DataFrame格式
print(result)
#results=list(result)
for it in result:
    res = {}
    res0=[]
    print(it[0])
    id=it[0]

    service=it[1]
    hostIP = it[3]
    port = it[4]

    print(id,service,hostIP,port)

    #####
    #if len(endTime)!=0:
        #endTime = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')
        #eflg=1

    #if len(startTime)!=0:
        #startTime = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
        #while datetime.datetime.now() < startTime:
            #time.sleep(1)
    #else:
         #pass
    #if repeatTimes != 0:
        #for i in range(repeatTimes):
            #scan(id,service,hostIP,port)

            #if eflag == 1:
                #if datetime.datetime.now() > endTime:
                    #break

    scan(id,service,hostIP,port)












#保存到数据库




