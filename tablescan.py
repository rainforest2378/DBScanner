from flask import Flask
from flask import request
import json
import nmap
import pymysql
import time, datetime
# 创建flask对象
#从数据库读取信息

import pymysql
#import pandas as pd
def ff6(s):
    s = s.replace('\t', '\\x09')
    s = s.replace('\n', '\\x0A')
    s = s.replace('\r', '\\x0D')
    for i in range(len(s)):
        if (s[i].isalpha() or s[i] == '_' or s[i] == '\\' or s[i].isdigit() or s[i] == '\'' or s[i] == '(' or s[
            i] == ')' or s[i] == ','):
            pass
        else:
            # print(hex((ord(a[i]))))
            a = hex((ord(s[i])))
            a = a.replace('0x', '\\x')
            s = s.replace(s[i], a)
    #print(s)
    s1 = ''

    i = 0

    while i < len(s):

        if s[i] == '\\':
            s1 += s[i] + s[i + 1] + s[i + 2] + s[i + 3]
            i += 4
            continue

        elif s[i] != '\\':
            a = hex((ord(s[i])))
            a = a.replace('0x', '\\x')
            s1 += a
            i += 1

    # data.decode('hex')
    #print(s1.encode('utf-8'))
    s2 = s1.encode('utf-8')
    # print(binascii.unhexlify(s1))
    s1 = s1.replace('\\x', '')
    #print(len(s2))
    #print(len(s1))
    #print(s1)

    num = ''
    num = num + s1[0] + s1[1]
    n = int(num, 16)
    #print(n)
    i = 8
    field = ['Field', 'Type ', 'Null', 'Key', 'Default', 'Extra']
    d = {}
    all = []
    flag = 0
    # print(chr(n1))
    #print(field[flag])
    while i < len(s1):
        #print(n)

        #print(flag)
        while n != 0:
            num1 = ''
            num1 = num1 + s1[i] + s1[i + 1]
            if num1=='FB':
                d[field[flag]]='NULL'
                flag+=1
                n-=1
                i+=2
                continue
            n1 = int(num1, 16)
            print(n1)

            # print(chr(n1))
            i += 2
            n -= 1
            a = ''
            while n1 != 0:
                x = ''
                x = x + s1[i] + s1[i + 1]
                b = chr(int(x, 16))
                n1 -= 1
                n -= 1
                a = a + b
                i += 2
            #print(a)
            d[field[flag]] = a
            flag += 1

        flag = 0
        all.append(d)
        print(d)
        d = {}
        num = ''
        num = num + s1[i] + s1[i + 1]
        n = int(num, 16)
        i = i + 8
    print(all)
    all=str(all)
    all1=''
    for i in range(len(all)):
        if all[i]=='[' or  all[i]==']'  :
            continue
        all1+=all[i]
    print(all1)
    return all1


# 功能函数
#开始扫描服务信息
def scan(host,db,table):
    host='192.168.43.143'
    #db='performance_schema'
    #table='data_locks'
    # result_str = "%s今年%s岁" % (name, age)
    print('----------------------------------------------------')

    print('----------------------------------------------------')
    nm = nmap.PortScanner(nmap_search_path=('nmap',r'D:\Nmap\nmap.exe'))
    argu = '--script mysqldatabase4x --script-args mysqluser=root,mysqlpass=root,db=%s,tab=%s' % \
            (db, table)
    dbase=db

    a = nm.scan(hosts=host,
                arguments=argu,
                ports='3306')


    for host in nm.all_hosts():  # 遍历扫描主机

        print('----------------------------------------------------')
        print('Host : %s (%s)' % (host, nm[host].hostname()))  # 输出主机及主机名
        print('State : %s' % nm[host].state())  # 输出主机状态，如up、down
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
                output=nm[host][proto][sport]['script']
                port = sport
                print('port : %s\t state : %s\t service: %s\t version: %s  output:%s' % (port, portstate, service, version, output))
                #print(output['mysqldatabase2'])
                o=output['mysqldatabase4x']
                res=ff6(o)

                tableName=table
                serviceIP=host
                servicePort='3306'
                #tableStruct = json.dumps(res)
                tableStruct = res
                #print(len(tableStruct))
                DBName=dbase
                #print(DBName)
                serviceName='mysql'
                sql = "insert into tableStruct(tableName,serviceIP,servicePort,serviceName,DBName,tableStruct) VALUE (%s,%s,%s,%s,%s,%s);"
                cursor.execute(sql, (tableName,serviceIP,servicePort,serviceName,DBName,tableStruct))
                conn.commit()








# 连接配置信息
conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                       passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
cursor = conn.cursor()
print('Program now starts on %s')
print('Executing...')
host=input("please input host:" )
db=input(" please input db:" )
table=input(" please input table:" )
scan(host,db,table)










#保存到数据库




