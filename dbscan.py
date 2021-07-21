
import json
import nmap
import time, datetime


import pymysql





# 功能函数
#开始扫描服务信息
def service_scan_controller(IPRange,DBServiceType,startTime, intervalTime, endTime, repeatTimes, enable):
    if enable==0:
        return 0
    print('startTime',startTime)

    #current_time= datetime.datetime.now()
    while datetime.datetime.now() < startTime:
        time.sleep(1)
    previous_time = datetime.datetime.now()
    service_scan(IPRange)
    if datetime.datetime.now() >= endTime:
        return 0
    if repeatTimes != 0:
        for i in range(repeatTimes):
            while (datetime.datetime.now() - previous_time).seconds < int(intervalTime) * 60:
                time.sleep(1)
            previous_time = datetime.datetime.now()
            service_scan(IPRange)
            # previous_time=datetime.datetime.now()
            if datetime.datetime.now() >= endTime:
                return 0

def service_scan(hostIP):
    print('start scan process:')
    print('----------------------------------------------------')

    nm = nmap.PortScanner(nmap_search_path=('nmap', r'/usr/share/nmap'))

    sc = datetime.date.today().strftime("%Y-%m-%d")
    wd = hostIP.split('.')[2]
    arg = '-sV -sC -A -oN %s-dblog%s' % (wd, sc)
    nm.scan(hosts=hostIP, arguments=arg, ports='3306')
    conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')

    cursor = conn.cursor()

    for host in nm.all_hosts():  # 遍历扫描主机

        for proto in nm[host].all_protocols():  # 遍历扫描协议，如tcp、udp

            protocal = proto
            lport = nm[host][proto].keys()  # 获取协议的所有扫描端口
            sorted(lport)  # 端口列表排序

            for sport in lport:  # 遍历端口及输出端口与状态，服务和版本信息
                service = nm[host][proto][sport]['name']
                product = nm[host][proto][sport]['product']
                s = " "
                version = product + s + nm[host][proto][sport]['version']


                if service == "mysql" or service == "memcache" or service == "mongod" or service == "redis" or service == "thrift-binary":
                    # scanDate= datetime.date.today().strftime("%Y-%m-%d")
                    scanTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    sql1 = "insert into service_detection(service,version,hostIP,port,foundTime,protocal) VALUE (%s,%s,%s,%s,%s,%s)"

                    cursor.execute(sql1, (service, version, host, sport, scanTime, protocal))
                    conn.commit()
    print('-------------------finish----------------------------')

    cursor.close()
    conn.close()

def db_tables_scan_controller(IP,port,user,password, startTime, intervalTime, endTime, repeatTimes, enable):
    if enable == 0:
        return 0

    # current_time= datetime.datetime.now()
    while datetime.datetime.now() < startTime:
        time.sleep(1)

    previous_time = datetime.datetime.now()
    db_tables_scan(IP,port,user,password)
    if datetime.datetime.now() >= endTime:
        return 0
    if repeatTimes != 0:
        for i in range(repeatTimes):
            while (datetime.datetime.now() - previous_time).seconds < int(intervalTime)*60:
                time.sleep(1)
            previous_time = datetime.datetime.now()
            db_tables_scan(IP,port,user,password)
            # previous_time=datetime.datetime.now()
            if datetime.datetime.now() >= endTime:
                return 0


def db_tables_scan(hostIP, port, user, password):
    # result_str = "%s今年%s岁" % (name, age)
    print('-----------------db-table scan start-----------------------------------')

    print('----------------------------------------------------')
    nm = nmap.PortScanner(nmap_search_path=('nmap', r'/usr/share/nmap'))
    #nm = nmap.PortScanner()
    print('-------nm-----')

    if user == '' or password == '':
        print('return')
        return 0
    arg = '--script fyl-mysql-databases --script-args mysqluser=%s,mysqlpass=%s' % (user, password)
    print(arg)
    nm.scan(hosts=hostIP, arguments=arg, ports=port)
    DBNames=[]
    tableNames={}

    for host in nm.all_hosts():  # 遍历扫描主机

        for proto in nm[host].all_protocols():  # 遍历扫描协议，如tcp、udp
            lport = nm[host][proto].keys()  # 获取协议的所有扫描端口
            sorted(lport)  # 端口列表排序

            for sport in lport:  # 遍历端口及输出端口与状态，服务和版本信息
                try:
                    output = nm[host][proto][sport]['script']

                    db = output['fyl-mysql-databases']
                    print(db)
                    db=db.strip().split('\n')
                    for i in range(len(db)):
                        #print(i)
                        #print(db[i])
                        DBNames.append(db[i].strip())

                except:
                    return 0

                for i in range(len(DBNames)):
                    #print(DBNames[i])
                    argu = '--script fyl2 --script-args mysqluser=%s,mysqlpass=%s,db=%s' % (user, password, DBNames[i])
                    a = nm.scan(hosts=host, arguments=argu,ports=port)
                    #print(a)
                    #print(nm)

                    #for host in nm.all_hosts():  # 遍历扫描主
                    for proto in a['scan'][host].all_protocols():  # 遍历扫描协议，如tcp、udp
                        lport = a['scan'][host][proto].keys()  # 获取协议的所有扫描端口
                        sorted(lport)  # 端口列表排序

                        for sport in lport:  # 遍历端口及输出端口与状态，服务和版本信息
                            try:
                                tables = a['scan'][host][proto][sport]['script']['fyl2']

                            except:
                                tables=''
                                #print('error')
                                #return 0
                            table_list = tables.strip().split('\n')
                            #print(table_list)
                            tl = []
                            for t in table_list:
                                tl.append(t.strip())
                            tableNames[DBNames[i]] = tl




                # res0 = ','.join(res0)
                # print(res)

                #print(res)
                # data0='|'.join(res0)

                # data0=json.dumps(res0)
                #data = json.dumps(res)
    DBNames=json.dumps(DBNames)
    tableNames=json.dumps(tableNames)
    foundTime=datetime.datetime.now()
    conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')

    cursor = conn.cursor()
    sql = "insert into db_tables(serviceIP,servicePort,DBNames,tableNames,foundTime) VALUE (%s,%s,%s,%s,%s)"

    cursor.execute(sql, (hostIP,port,DBNames,tableNames,foundTime))
    conn.commit()
    cursor.close()
    conn.close()
    print('scan ok')

# 连接配置信息


def table_struct_scan_controller(IP,port,user,password, DBName,tableName,startTime, intervalTime, endTime, repeatTimes, enable):
    if enable == 0:
        return 0

    # current_time= datetime.datetime.now()
    while datetime.datetime.now() < startTime:
        time.sleep(1)

    previous_time = datetime.datetime.now()
    table_struct_scan(IP,port,user,password,DBName,tableName)
    if datetime.datetime.now() >= endTime:
        return 0
    if repeatTimes != 0:
        for i in range(repeatTimes):
            while (datetime.datetime.now() - previous_time).seconds < int(intervalTime)*60:
                time.sleep(1)
            previous_time = datetime.datetime.now()
            db_tables_scan(IP,port,user,password,DBName,tableName)
            # previous_time=datetime.datetime.now()
            if datetime.datetime.now() >= endTime:
                return 0

def table_struct_scan(host,port,user,password,DBName,tableName):
    # result_str = "%s今年%s岁" % (name, age)
    if user == '' or password == '':
        return 0
    print('--------------table struct scan start--------------------')
    field = ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra']
    print('--------------nm--------------------')

    #nm = nmap.PortScanner(nmap_search_path=('nmap',r'D:\Nmap\nmap.exe'))
    nm = nmap.PortScanner(nmap_search_path=('nmap', r'/usr/share/nmap'))
    arg='--script fyl3 --script-args mysqluser=%s,mysqlpass=%s,db=%s,table=%s'%(user,password,DBName,tableName)
    print('--------------arg--------------------')
    print(arg)
    nm.scan(hosts=host, arguments=arg, ports=port)
    print('nm.scan')
    tableStruct=[]
    for host in nm.all_hosts():  # 遍历扫描主机


        for proto in nm[host].all_protocols():  # 遍历扫描协议，如tcp、udp
            lport = nm[host][proto].keys()  # 获取协议的所有扫描端口
            sorted(lport)  # 端口列表排序

            for sport in lport:  # 遍历端口及输出端口与状态，服务和版本信息
                try:
                    output = nm[host][proto][sport]['script']
                    db = output['fyl3']
                    #print(db)
                    #print(type(db))
                    ab=db.strip().split('\n')
                    print('------------------')
                    print(ab)
                    for i in ab:
                        record=i.split(',')
                        #print(len(record))
                        d={}
                        for i in range(6):
                            d[field[i]]=record[i].strip()
                            #print(d)

                        tableStruct.append(d)




                except:
                    return 0


                tableStruct = json.dumps(tableStruct)
                print(tableStruct)
                #tableNames = json.dumps(tableNames)
                foundTime = datetime.datetime.now()
                conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                                       passwd='fyl@chjtxmysql', db='fyl', charset='utf8')

                cur = conn.cursor()
                sql = "insert into table_struct(serviceIP,servicePort,DBName,tableName,tableStruct,foundTime) VALUE (%s,%s,%s,%s,%s,%s)"

                cur.execute(sql, (host, port, DBName, tableName,tableStruct, foundTime))
                conn.commit()
                cur.close()
                conn.close()
                print('scan ok')



#db_tables_scan('10.10.103.150','3306','root','123456')





#保存到数据库




