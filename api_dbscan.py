#!/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import OrderedDict
from flask import Flask, jsonify
from flask import request
#from flask_sqlalchemy import SQLAlchemy
#import sqlalchemy
import json
#import nmap
import time, datetime
import pymysql
import logging
# 创建flask对象
import IPy
#from logging import handlers

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
#logging.basicConfig(filename='my.log', level=logging.DEBUG, format=LOG_FORMAT)

from logging.handlers import TimedRotatingFileHandler



import re
def is_time(time):
    check_time=re.compile(('^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])\s+(20|21|22|23|[0-1]\d):[0-5]\d:[0-5]\d$'))
    if check_time.match(time):
        return True
    else:
        return False

def is_ip(ipAddr):
    check_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    if check_ip.match(ipAddr):
        return True
    else:
        return False

@app.route("/DBservice/api/scheduler/DBservice", methods=["POST"])
def check2():

#    app.logger.info(json.dumps({
 #       "AccessLog": {
  #          #"status_code": response.status_code,
   #         "method": request.method,
    #        "ip": request.headers.get('X-Real-Ip', request.remote_addr),
     #       "url": request.url,
      #      "referer": request.headers.get('Referer'),
       #     "agent": request.headers.get("User-Agent"),
        #    #"requestId": str(g.requestId),
    #    }
   # }))

    # 默认返回内容
    return_dict = {'status': 'ok'}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)

    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    print(get_Data)
    IPRange = get_Data.get('IPRange')
    if IPRange is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'IP为空'
        return json.dumps(return_dict, ensure_ascii=False)
    try:
        a = IPy.IP(IPRange)
    except Exception as e:
        #print('str(Exception):\t', str(Exception))
        return_dict['status'] = 'error'
        return_dict['reason'] = str(e)
        return json.dumps(return_dict, ensure_ascii=False)
        #print('repr(e):\t', repr(e))
        # print('e.message:\t', e.message)
        # print('traceback.print_exc():', traceback.print_exc())
        #print('traceback.format_exc():\n%s' % traceback.format_exc())

    DBServiceType = get_Data.get('DBServiceType')
    if DBServiceType is None:
        DBServiceType='1|2|3|4|5'
    startTime = get_Data.get('startTime')
    if startTime is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'startTime为空'
    if startTime != None and is_time(startTime)==False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)

    intervalTime = get_Data.get('intervalTime')
    if intervalTime is None:
        intervalTime = 60
    endTime = get_Data.get('endTime')
    if endTime is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'endTime为空'
        return json.dumps(return_dict, ensure_ascii=False)
    if endTime != None and is_time(endTime)==False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)

    repeatTimes = get_Data.get('repeatTimes')
    if repeatTimes is None:
        repeatTimes = 0
    enable = get_Data.get('enable')
    if enable is None:
        enable = 1



    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    sql = "insert into service_schedule(IPRange,DBServiceType,startTime,intervalTime,endTime,repeatTimes,enable,createTime,lastUpdate) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    createTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lastUpdate=createTime
    cursor.execute(sql, (IPRange,DBServiceType,startTime,intervalTime,endTime,repeatTimes,enable,createTime,lastUpdate))

    # 最新插入行的主键id
    #print(cursor.lastrowid)
    id=conn.insert_id()


    #logger.info('Adding config information is completed')
    conn.commit()  # 把修改的数据提交到数据库

    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接
    # enable=get_Data.get('enable')
    # 对参数进行操作

    #print('Program now starts on %s' % startTime)
    #Sprint('Executing...')
    return_dict['scheduleID']=id
    return_dict["IPRange"]=IPRange
    return_dict["DBServiceType"]=DBServiceType
    return_dict["startTime"]=startTime
    return_dict["intervalTime"]=intervalTime
    return_dict["endTime"]=endTime
    return_dict["repeatTimes"]=repeatTimes
    return_dict["enable"]=enable
    return_dict["createTime"]=createTime

    return jsonify(return_dict)

@app.route("/DBservice/api/scheduler/DBservice/<int:scheduleID>", methods=["PUT"])
def check1(scheduleID):
    app.logger.info(json.dumps({
        "AccessLog": {
            # "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            # "requestId": str(g.requestId),
        }
    }))
    # 默认返回内容
    return_dict= {'status': 'ok'}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json

    get_Data = json.loads(get_Data)


    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    sqlo='UPDATE service_schedule '
    set_list=[]
    where_list=[]

    IPRange = get_Data.get('IPRange')
    #print(scheduleID)
    #print(IPRange)
    if IPRange!=None:
        try:
            a = IPy.IP(IPRange)
        except Exception as e:
            # print('str(Exception):\t', str(Exception))
            return_dict['status'] = 'error'
            return_dict['reason'] = str(e)
            return json.dumps(return_dict, ensure_ascii=False)

        set_list.append('IPRange')
        where_list.append(IPRange)
        #cursor.execute("UPDATE service_schedule SET IPRange=%s WHERE id=%s",(IPRange,scheduleID))
    DBServiceType = get_Data.get('DBServiceType')
    if DBServiceType != None:
        set_list.append('DBServiceType')
        where_list.append(DBServiceType)
        #cursor.execute("UPDATE service_schedule SET DBServiceType=%s WHERE id=%s",(DBServiceType,scheduleID))
    startTime = get_Data.get('startTime')
    if startTime != None and is_time(startTime)==False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)
    if startTime !=None:
        set_list.append('startTime')
        where_list.append(startTime)
        #cursor.execute(" UPDATE service_schedule SET startTime=%s WHERE id=%s",(startTime,scheduleID))
    intervalTime = get_Data.get('intervalTime')
    if intervalTime != None:
        set_list.append('intervalTime')
        where_list.append(intervalTime)
        #cursor.execute(" UPDATE service_schedule SET intervalTime=%s WHERE id=%s",(intervalTime,scheduleID))
    endTime = get_Data.get('endTime')
    if endTime != None and is_time(endTime)==False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)
    if endTime != None:
        set_list.append('endTime')
        where_list.append(endTime)
        #cursor.execute("UPDATE service_schedule SET endTime=%s WHERE id=%s",(endTime,scheduleID))
    repeatTimes = get_Data.get('repeatTimes')
    if repeatTimes != None:
        set_list.append('repeatTimes')
        where_list.append(repeatTimes)
        #cursor.execute("UPDATE service_schedule SET repeatTimes=%s WHERE id=%s",(repeatTimes,scheduleID))
    enable = get_Data.get('enable')
    if enable != None:
        set_list.append('enable')
        where_list.append(enable)
        #cursor.execute("UPDATE service_schedule SET enable=%s WHERE id=%s",(enable,scheduleID))

    lastUpdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sqlo=sqlo+' SET lastUpdate=\'%s\''%lastUpdate
    #sqlo=sqlo+' set'
    if len(set_list)!=0:
        for i in range(len(set_list)):
            sqlo=sqlo+' , '+'%s = \'%s\''% (set_list[i],where_list[i])
    sqlo=sqlo+' where id=%s'%scheduleID
    print(sqlo)
    cursor.execute(sqlo)
    #cursor.execute(" UPDATE service_schedule SET serviceName=%s,startTime=%s,intervalTime=%s,endTime=%s,repeatTimes=%s,enable=%s WHERE id=%s" , (scheduleID,configTime, serviceName, startTime, intervalTime, endTime, repeatTimes, enable, ConfigID))
    conn.commit()  # 把修改的数据提交到数据库
    #logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        #level=logging.DEBUG)

    #logger.info('Updating config information is completed。')
    cursor.execute("select * from service_schedule where id=%s",(scheduleID))
    results = cursor.fetchall()
    if len(results)!=0:
        for row in results:
            sid = row[0]
            IPRange = row[1]
            DBServiceType = row[2]
            startTime = row[3]
            intervalTime = row[4]
            endTime = row[5]
            repeatTimes = row[6]
            enable = row[7]
            createTime = row[8]
            lastUpdate = row[9]

        return_dict['scheduleID'] = sid
        return_dict["IPRange"] = IPRange
        return_dict["DBServiceType"] = DBServiceType
        return_dict["startTime"] = str(startTime)
        return_dict["intervalTime"] = intervalTime
        return_dict["endTime"] = str(endTime)
        return_dict["repeatTimes"] = repeatTimes
        return_dict["enable"] = enable
        return_dict["createTime"] = str(createTime)
        return_dict["lastUpdate"] = str(lastUpdate)
    else:
        pass


    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接

    return jsonify(return_dict)

    #return json.dumps(return_dict, ensure_ascii=False)

@app.route("/DBservice/api/scheduler/DBservice/read", methods=["GET"])
@app.route("/DBservice/api/scheduler/DBservice/read/<int:scheduleID>", methods=["GET"])
def check(scheduleID=None):
    app.logger.info(json.dumps({
        "AccessLog": {
            # "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            # "requestId": str(g.requestId),
        }
    }))



    # 默认返回内容
    #user_list = db.session.query(User).all()  # 查询所有。 query(User)表示查询所有列
    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    return_dict={"rcode":'200',"msg":"successful"}

    if scheduleID != None:
        sql_page = "select * from service_schedule where id =%d"%scheduleID
        totalCountOk = cursor.execute(sql_page)
        if totalCountOk:
            result = cursor.fetchall()
            pagenums = len(result)
            service_schedule = []
            for row in result:
                sid = row[0]
                IPRange = row[1]
                DBServiceType = row[2]
                startTime = row[3]
                intervalTime = row[4]
                endTime = row[5]
                repeatTimes = row[6]
                enable = row[7]
                createTime = row[8]
                lastUpdate = row[9]
                return_dict['data']={'scheduleID': sid, "IPRange": IPRange, "DBServiceType": DBServiceType, "startTime": str(startTime),
                 "intervalTime": intervalTime,
                 "endTime": str(endTime), "repeatTimes": repeatTimes, "enable": enable,
                 "createTime": str(createTime), "lastUpdate": str(lastUpdate)}
            return jsonify(return_dict)
        else:
            return jsonify(return_dict)

    sql = 'select * from service_schedule;'


    pageSize = 10
    totalCount = -1
    totalPageNum = -1

    pageNumber = 1
    pageIndex = pageNumber - 1
    offset = pageSize * pageIndex


    #totalCountSql = "SELECT COUNT(*) from `user_storybook_list` WHERE `userId`=%d" % userId
    totalCountOk=cursor.execute(sql)
    totalCount = totalCountOk
    if totalCount > 0:
        totalPageNum = int(totalCount / pageSize)
        if (totalCount % pageSize) > 0:
            totalPageNum += 1
    print('totalPageNum', totalPageNum)

        #if pageNumber > totalPageNum:
         #   return ( "Current page number %d exceed max page number %d" % (
          #      pageNumber, totalPageNum))

    sql_page = "select * from service_schedule LIMIT %d OFFSET %d" % (pageSize, offset)
    totalCountOk = cursor.execute(sql_page)
    if totalCountOk:
        result = cursor.fetchall()
        pagenums = len(result)
        service_schedule = []
        for row in result:
            sid = row[0]
            IPRange = row[1]
            DBServiceType = row[2]
            startTime = row[3]
            intervalTime = row[4]
            endTime = row[5]
            repeatTimes = row[6]
            enable = row[7]
            createTime = row[8]
            lastUpdate = row[9]

            d = {'scheduleID': sid, "IPRange": IPRange, "DBServiceType": DBServiceType, "startTime": str(startTime),
                 "intervalTime": intervalTime,
                 "endTime": str(endTime), "repeatTimes": repeatTimes, "enable": enable,
                 "createTime": str(createTime), "lastUpdate": str(lastUpdate)}

            service_schedule.append(d)
        return_data = {

                "total_num": totalCount,
                "page_num": pageNumber,
                "num": pagenums,
                'service_schedules': service_schedule,
            }
        return_dict["data"] =return_data


    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接



    #return_dict=json.loads(json.dumps(return_dict), object_pairs_hook=OrderedDict)

    return jsonify(return_dict)

    # 对参数进行操作

@app.route("/table/api/scheduler/DBTables", methods=["POST"])
def check_table2():
    app.logger.info(json.dumps({
        "AccessLog": {
            # "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            # "requestId": str(g.requestId),
        }
    }))
    # 默认返回内容
    return_dict = {'status': 'ok'}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    IP = get_Data.get('IP')
    if IP is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'IP为空'
        return json.dumps(return_dict, ensure_ascii=False)
    if is_ip(IP)==False:
        #print('str(Exception):\t', str(Exception))
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong IP format.'
        return json.dumps(return_dict, ensure_ascii=False)

    port = get_Data.get('port')
    if port is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'port为空'
        return json.dumps(return_dict, ensure_ascii=False)
    user = get_Data.get('user')
    if user is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'user为空'
        return json.dumps(return_dict, ensure_ascii=False)
    password = get_Data.get('password')
    if password is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'password为空'
        return json.dumps(return_dict, ensure_ascii=False)

    startTime = get_Data.get('startTime')
    if startTime is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'startTime为空'
    if startTime != None and is_time(startTime) == False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)
    intervalTime = get_Data.get('intervalTime')
    if intervalTime is None:
        intervalTime = 60
    endTime = get_Data.get('endTime')
    if endTime is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'endTime为空'
        return json.dumps(return_dict, ensure_ascii=False)
    if endTime != None and is_time(endTime) == False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)
    repeatTimes = get_Data.get('repeatTimes')
    if repeatTimes is None:
        repeatTimes = 0
    enable = get_Data.get('enable')
    if enable is None:
        enable = 1


    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    sql = "insert into db_tables_schedule(IP,port,user,password,startTime,intervalTime,endTime,repeatTimes,enable,createTime,lastUpdate) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

    createTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lastUpdate=createTime
    cursor.execute(sql, (IP,port,user,password,startTime,intervalTime,endTime,repeatTimes,enable,createTime,lastUpdate))

    # 最新插入行的主键id
    #print(cursor.lastrowid)
    id=conn.insert_id()
    #print(id)

    #logger.info('Adding config information is completed')
    conn.commit()  # 把修改的数据提交到数据库

    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接
    # enable=get_Data.get('enable')
    # 对参数进行操作

    #print('Program now starts on %s' % startTime)
    #Sprint('Executing...')
    return_dict['scheduleID']=id
    return_dict["IP"]=IP
    return_dict["port"]=port
    return_dict["user"] = user
    return_dict["password"] = password
    return_dict["startTime"]=startTime
    return_dict["intervalTime"]=intervalTime
    return_dict["endTime"]=endTime
    return_dict["repeatTimes"]=repeatTimes
    return_dict["enable"]=enable
    return_dict["createTime"]=createTime

    return jsonify(return_dict)


@app.route("/table/api/scheduler/DBTables/<int:scheduleID>", methods=["PUT"])
def check_table1(scheduleID):
    app.logger.info(json.dumps({
        "AccessLog": {
            # "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            # "requestId": str(g.requestId),
        }
    }))
    # 默认返回内容
    return_dict= {'status': 'ok'}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json

    get_Data = json.loads(get_Data)

    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()

    sqlo = 'UPDATE db_tables_schedule '
    set_list = []
    where_list = []

    IP= get_Data.get('IP')

    if IP != None:
        if is_ip(IP) == False:
            # print('str(Exception):\t', str(Exception))
            return_dict['status'] = 'error'
            return_dict['reason'] = 'Wrong IP format.'
            return json.dumps(return_dict, ensure_ascii=False)
        #cursor.execute("UPDATE db_tables_schedule SET IP=%s WHERE id=%s",(IP,scheduleID))
        set_list.append('IP')
        where_list.append(IP)
    port = get_Data.get('port')
    if port != None:
        #cursor.execute("UPDATE db_tables_schedule SET port=%s WHERE id=%s",(port,scheduleID))
        set_list.append('port')
        where_list.append(port)
    user = get_Data.get('user')
    if user != None:
        #cursor.execute("UPDATE db_tables_schedule SET user=%s WHERE id=%s",(user,scheduleID))
        set_list.append('user')
        where_list.append(user)
    password = get_Data.get('password')
    if password != None:
        #cursor.execute("UPDATE db_tables_schedule SET password=%s WHERE id=%s",(password,scheduleID))
        set_list.append('password')
        where_list.append(password)
    startTime = get_Data.get('startTime')
    if startTime != None and is_time(startTime)==False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)
    if startTime != None:
        set_list.append('startTime')
        where_list.append(startTime)
        #cursor.execute(" UPDATE db_tables_schedule SET startTime=%s WHERE id=%s",(startTime,scheduleID))
    intervalTime = get_Data.get('intervalTime')
    if intervalTime != None:
        set_list.append('intervalTime')
        where_list.append(intervalTime)
        #cursor.execute(" UPDATE db_tables_schedule SET intervalTime=%s WHERE id=%s",(intervalTime,scheduleID))
    endTime = get_Data.get('endTime')
    if endTime != None and is_time(endTime)==False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)
    if endTime != None:
        set_list.append('endTime')
        where_list.append(endTime)
        #cursor.execute("UPDATE service_schedule SET endTime=%s WHERE id=%s",(endTime,scheduleID))
    repeatTimes = get_Data.get('repeatTimes')
    if repeatTimes != None:
        set_list.append('repeatTimes')
        where_list.append(repeatTimes)
        #cursor.execute("UPDATE db_tables_schedule SET repeatTimes=%s WHERE id=%s",(repeatTimes,scheduleID))
    enable = get_Data.get('enable')
    if enable != None:
        set_list.append('enable')
        where_list.append(enable)
        #cursor.execute("UPDATE db_tables_schedule SET enable=%s WHERE id=%s",(enable,scheduleID))

    lastUpdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sqlo = sqlo + ' SET lastUpdate=\'%s\'' % lastUpdate
    # sqlo=sqlo+' set'
    if len(set_list) != 0:
        for i in range(len(set_list)):
            sqlo = sqlo + ' , ' + '%s = \'%s\'' % (set_list[i], where_list[i])
    sqlo = sqlo + ' where id=%s' % scheduleID
    print(sqlo)
    cursor.execute(sqlo)

    #cursor.execute(" UPDATE service_schedule SET serviceName=%s,startTime=%s,intervalTime=%s,endTime=%s,repeatTimes=%s,enable=%s WHERE id=%s" , (scheduleID,configTime, serviceName, startTime, intervalTime, endTime, repeatTimes, enable, ConfigID))
    conn.commit()  # 把修改的数据提交到数据库
    #logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        #level=logging.DEBUG)

    #logger.info('Updating config information is completed。')
    cursor.execute("select * from db_tables_schedule where id=%s",(scheduleID))
    results = cursor.fetchall()
    if len(results)!=0:
        for row in results:
            sid = row[0]
            IP = row[1]
            port = row[2]
            user = row[3]
            password = row[4]
            startTime = row[5]
            intervalTime = row[6]
            endTime = row[7]
            repeatTimes = row[8]
            enable = row[9]
            createTime = row[10]
            lastUpdate = row[11]
        return_dict['scheduleID'] = sid
        return_dict["IP"] = IP
        return_dict["port"] = port
        return_dict["user"] = user
        return_dict["password"] = password
        return_dict["startTime"] = str(startTime)
        return_dict["intervalTime"] = intervalTime
        return_dict["endTime"] = str(endTime)
        return_dict["repeatTimes"] = repeatTimes
        return_dict["enable"] = enable
        return_dict["createTime"] = str(createTime)
        return_dict["lastUpdate"] = str(lastUpdate)
    else:
        pass




    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接

    return jsonify(return_dict)

    #return json.dumps(return_dict, ensure_ascii=False)

@app.route("/table/api/scheduler/DBTables/read/", methods=["GET"])
@app.route("/table/api/scheduler/DBTables/read/<int:scheduleID>", methods=["GET"])
def check_table(scheduleID=None):
    app.logger.info(json.dumps({
        "AccessLog": {
            # "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            # "requestId": str(g.requestId),
        }
    }))
    # 默认返回内容
    #user_list = db.session.query(User).all()  # 查询所有。 query(User)表示查询所有列
    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    return_dict={"rcode":'200',"msg":"successful"}

    if scheduleID != None:
        sql_page = "select * from db_tables_schedule where id =%d"%scheduleID
        totalCountOk = cursor.execute(sql_page)
        if totalCountOk:
            result = cursor.fetchall()
            pagenums = len(result)
            service_schedule = []
            for row in result:
                sid=row[0]
                IP = row[1]
                port = row[2]
                user = row[3]
                password = row[4]
                startTime = row[5]
                intervalTime = row[6]
                endTime = row[7]
                repeatTimes = row[8]
                enable = row[9]
                createTime = row[10]
                lastUpdate = row[11]

                return_dict['data'] = {'scheduleID': sid, "IP": IP, "port": port, "user": user, "password": password,
                     "startTime": str(startTime),
                     "intervalTime": intervalTime,
                     "endTime": str(endTime), "repeatTimes": repeatTimes, "enable": enable,
                     "createTime": str(createTime), "lastUpdate": str(lastUpdate)}

            return jsonify(return_dict)
        else:
            return jsonify(return_dict)





    sql = 'select * from db_tables_schedule;'

    pageSize = 10
    totalCount = -1
    totalPageNum = -1

    pageNumber = 1
    pageIndex = pageNumber - 1
    offset = pageSize * pageIndex


    #totalCountSql = "SELECT COUNT(*) from `user_storybook_list` WHERE `userId`=%d" % userId
    totalCountOk=cursor.execute(sql)
    totalCount = totalCountOk
    if totalCount > 0:
        totalPageNum = int(totalCount / pageSize)
        if (totalCount % pageSize) > 0:
            totalPageNum += 1
    print('totalPageNum', totalPageNum)

        #if pageNumber > totalPageNum:
         #   return ( "Current page number %d exceed max page number %d" % (
          #      pageNumber, totalPageNum))

    #for p in range(totalPageNum):

    sql_page = "select * from db_tables_schedule LIMIT %d OFFSET %d" % (pageSize, offset)
    totalCountOk = cursor.execute(sql_page)
    if totalCountOk:
        result = cursor.fetchall()
        pagenums=len(result)
        service_schedule = []
        for row in result:
            sid = row[0]
            IP = row[1]
            port = row[2]
            user = row[3]
            password = row[4]
            startTime = row[5]
            intervalTime = row[6]
            endTime = row[7]
            repeatTimes = row[8]
            enable = row[9]
            createTime = row[10]
            lastUpdate = row[11]

            d = {'scheduleID': sid, "IP": IP, "port": port,"user":user,"password":password,"startTime": str(startTime),
                     "intervalTime": intervalTime,
                     "endTime": str(endTime), "repeatTimes": repeatTimes, "enable": enable,
                     "createTime": str(createTime), "lastUpdate": str(lastUpdate)}

            service_schedule.append(d)
        return_data = {

                    "total_num": totalCount,
                    "page_num": pageNumber,
                    "page_size":pageSize,
                    "num": pagenums,
                    'service_schedules': service_schedule,
                }
    #data.append(return_data)
        return_dict["data"] =return_data


    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接



    #return_dict=json.loads(json.dumps(return_dict), object_pairs_hook=OrderedDict)

    return jsonify(return_dict)

@app.route("/table/api/scheduler/tableStruct", methods=["POST"])
def check_struct2():
    app.logger.info(json.dumps({
        "AccessLog": {
            # "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            # "requestId": str(g.requestId),
        }
    }))


    # 默认返回内容
    return_dict = {'status': 'ok'}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    IP = get_Data.get('IP')
    if IP is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'IP为空'
        return json.dumps(return_dict, ensure_ascii=False)
    if is_ip(IP) == False:
        # print('str(Exception):\t', str(Exception))
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong IP format.'
        return json.dumps(return_dict, ensure_ascii=False)
    port = get_Data.get('port')
    if port is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'port为空'
        return json.dumps(return_dict, ensure_ascii=False)
    user = get_Data.get('user')
    if user is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'user为空'
        return json.dumps(return_dict, ensure_ascii=False)
    password = get_Data.get('password')
    if password is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'password为空'
        return json.dumps(return_dict, ensure_ascii=False)
    DBName = get_Data.get('DBName')
    if DBName is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'DBName为空'
        return json.dumps(return_dict, ensure_ascii=False)
    tableName = get_Data.get('tableName')
    if tableName is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'tableName为空'
        return json.dumps(return_dict, ensure_ascii=False)

    startTime = get_Data.get('startTime')
    if startTime is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'startTime为空'
    if startTime != None and is_time(startTime) == False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)

    intervalTime = get_Data.get('intervalTime')
    if intervalTime is None:
        intervalTime = 60
    endTime = get_Data.get('endTime')
    if endTime is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'endTime为空'
    if endTime != None and is_time(endTime) == False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)

    repeatTimes = get_Data.get('repeatTimes')
    if repeatTimes is None:
        repeatTimes = 0
    enable = get_Data.get('enable')
    if enable is None:
        enable = 1

    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    sql = "insert into table_struct_schedule(IP,port,user,password,DBName,tableName,startTime,intervalTime,endTime,repeatTimes,enable,createTime,lastUpdate) VALUE (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    createTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lastUpdate=createTime
    cursor.execute(sql, (IP,port,user,password,DBName,tableName,startTime,intervalTime,endTime,repeatTimes,enable,createTime,lastUpdate))

    # 最新插入行的主键id
    #print(cursor.lastrowid)
    id=conn.insert_id()


    #logger.info('Adding config information is completed')
    conn.commit()  # 把修改的数据提交到数据库

    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接
    # enable=get_Data.get('enable')
    # 对参数进行操作

    #print('Program now starts on %s' % startTime)
    #Sprint('Executing...')
    return_dict['scheduleID']=id
    return_dict["IP"]=IP
    return_dict["port"]=port
    return_dict["user"] = user
    return_dict["DBName"]=DBName
    return_dict["tableName"]=tableName
    return_dict["password"] = password
    return_dict["startTime"]=startTime
    return_dict["intervalTime"]=intervalTime
    return_dict["endTime"]=endTime
    return_dict["repeatTimes"]=repeatTimes
    return_dict["enable"]=enable
    return_dict["createTime"]=createTime

    return jsonify(return_dict)

@app.route("/table/api/scheduler/tableStruct/<int:scheduleID>", methods=["PUT"])
def check_struct1(scheduleID):
    app.logger.info(json.dumps({
        "AccessLog": {
            # "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            # "requestId": str(g.requestId),
        }
    }))
    # 默认返回内容
    return_dict= {'status': 'ok'}

    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['status'] = 'error'
        return_dict['reason'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json

    get_Data = json.loads(get_Data)

    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()

    sqlo = 'UPDATE table_struct_schedule '
    set_list = []
    where_list = []

    IP= get_Data.get('IP')
    if IP != None:
        try:
            a = IPy.IP(IP)
        except Exception as e:
            # print('str(Exception):\t', str(Exception))
            return_dict['status'] = 'error'
            return_dict['reason'] = str(e)
            return json.dumps(return_dict, ensure_ascii=False)
        set_list.append('IP')
        where_list.append(IP)
        #cursor.execute("UPDATE table_struct_schedule SET IP=%s WHERE id=%s",(IP,scheduleID))
    port = get_Data.get('port')
    if port != None:
        set_list.append('port')
        where_list.append(port)
        #cursor.execute("UPDATE table_struct_schedule SET port=%s WHERE id=%s",(port,scheduleID))
    user = get_Data.get('user')
    if user != None:
        set_list.append('user')
        where_list.append(user)
        #cursor.execute("UPDATE table_struct_schedule SET user=%s WHERE id=%s",(user,scheduleID))
    password = get_Data.get('password')
    if password != None:
        set_list.append('password')
        where_list.append(password)
        #cursor.execute("UPDATE table_struct_schedule SET password=%s WHERE id=%s",(password,scheduleID))
    DBName = get_Data.get('DBName')
    if DBName != None:
        set_list.append('DBName')
        where_list.append(DBName)
        #cursor.execute("UPDATE table_struct_schedule SET DBName=%s WHERE id=%s", (DBName, scheduleID))
    tableName = get_Data.get('tableName')
    if tableName != None:
        #cursor.execute("UPDATE table_struct_schedule SET tableName=%s WHERE id=%s", (tableName, scheduleID))
        set_list.append('tableName')
        where_list.append(tableName)
    startTime = get_Data.get('startTime')
    if startTime != None and is_time(startTime)==False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)
    if startTime != None:
        set_list.append('startTime')
        where_list.append(startTime)
        #cursor.execute(" UPDATE db_tables_schedule SET startTime=%s WHERE id=%s",(startTime,scheduleID))
    intervalTime = get_Data.get('intervalTime')
    if intervalTime != None:
        set_list.append('intervalTime')
        where_list.append(intervalTime)
        #cursor.execute(" UPDATE db_tables_schedule SET intervalTime=%s WHERE id=%s",(intervalTime,scheduleID))
    endTime = get_Data.get('endTime')
    if endTime != None and is_time(endTime)==False:
        return_dict['status'] = 'error'
        return_dict['reason'] = 'Wrong time format.eg:2020-01-26 12:00:00'
        return json.dumps(return_dict, ensure_ascii=False)
    if endTime != None:
        set_list.append('endTime')
        where_list.append(endTime)
        #cursor.execute("UPDATE service_schedule SET endTime=%s WHERE id=%s",(endTime,scheduleID))
    repeatTimes = get_Data.get('repeatTimes')
    if repeatTimes != None:
        set_list.append('repeatTimes')
        where_list.append(repeatTimes)
        #cursor.execute("UPDATE db_tables_schedule SET repeatTimes=%s WHERE id=%s",(repeatTimes,scheduleID))
    enable = get_Data.get('enable')
    if enable != None:
        set_list.append('enable')
        where_list.append(enable)
        #cursor.execute("UPDATE db_tables_schedule SET enable=%s WHERE id=%s",(enable,scheduleID))



    lastUpdate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sqlo = sqlo + ' SET lastUpdate=\'%s\'' % lastUpdate
    # sqlo=sqlo+' set'
    print(set_list)
    if len(set_list) != 0:
        for i in range(len(set_list)):
            sqlo = sqlo + ' , ' + '%s = \'%s\'' % (set_list[i], where_list[i])
    sqlo = sqlo + ' where id=%s' % scheduleID
    print(sqlo)
    cursor.execute(sqlo)

    #cursor.execute(" UPDATE service_schedule SET serviceName=%s,startTime=%s,intervalTime=%s,endTime=%s,repeatTimes=%s,enable=%s WHERE id=%s" , (scheduleID,configTime, serviceName, startTime, intervalTime, endTime, repeatTimes, enable, ConfigID))
    conn.commit()  # 把修改的数据提交到数据库
    #logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        #level=logging.DEBUG)

    #logger.info('Updating config information is completed。')
    cursor.execute("select * from table_struct_schedule where id=%s",(scheduleID))
    results = cursor.fetchall()
    if len(results)!=0:
        for row in results:
            sid = row[0]
            IP = row[1]
            port = row[2]
            user = row[3]
            password = row[4]
            DBName = row[5]
            tableName = row[6]

            startTime = row[7]
            intervalTime = row[8]
            endTime = row[9]
            repeatTimes = row[10]
            enable = row[11]
            createTime = row[12]
            lastUpdate = row[13]

        return_dict['scheduleID'] = sid
        return_dict["IP"] = IP
        return_dict["port"] = port
        return_dict["user"] = user
        return_dict["DBName"] = DBName
        return_dict["tableName"] = tableName
        return_dict["password"] = password
        return_dict["startTime"] = str(startTime)
        return_dict["intervalTime"] = intervalTime
        return_dict["endTime"] = str(endTime)
        return_dict["repeatTimes"] = repeatTimes
        return_dict["enable"] = enable
        return_dict["createTime"] = str(createTime)
        return_dict["lastUpdate"] = str(lastUpdate)
    else:
        pass


    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接

    return jsonify(return_dict)

    #return json.dumps(return_dict, ensure_ascii=False)

@app.route("/table/api/scheduler/tableStruct/read", methods=["GET"])
@app.route("/table/api/scheduler/tableStruct/read/<int:scheduleID>", methods=["GET"])
def check_struct(scheduleID=None):
    app.logger.info(json.dumps({
        "AccessLog": {
            # "status_code": response.status_code,
            "method": request.method,
            "ip": request.headers.get('X-Real-Ip', request.remote_addr),
            "url": request.url,
            "referer": request.headers.get('Referer'),
            "agent": request.headers.get("User-Agent"),
            # "requestId": str(g.requestId),
        }
    }))
    # 默认返回内容
    #user_list = db.session.query(User).all()  # 查询所有。 query(User)表示查询所有列
    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    return_dict={"rcode":'200',"msg":"successful"}
    if scheduleID != None:
        sql_page = "select * from table_struct_schedule where id =%d" % scheduleID
        totalCountOk = cursor.execute(sql_page)
        if totalCountOk:
            result = cursor.fetchall()
            pagenums = len(result)
            service_schedule = []
            for row in result:
                sid = row[0]
                IP = row[1]
                port = row[2]
                user = row[3]
                password = row[4]
                DBName = row[5]
                tableName = row[6]
                startTime = row[7]
                intervalTime = row[8]
                endTime = row[9]
                repeatTimes = row[10]
                enable = row[11]
                createTime = row[12]
                lastUpdate = row[13]

                return_dict['data'] =  {'scheduleID': sid, "IP": IP, "port": port, "user": user, "password": password,
                     "startTime": str(startTime),
                     'DBName': DBName, 'tableName': tableName,
                     "intervalTime": intervalTime,
                     "endTime": str(endTime), "repeatTimes": repeatTimes, "enable": enable,
                     "createTime": str(createTime), "lastUpdate": str(lastUpdate)}



            return jsonify(return_dict)
        else:
            return jsonify(return_dict)

    sql = 'select * from table_struct_schedule;'

    pageSize = 10
    totalCount = -1
    totalPageNum = -1

    pageNumber = 1
    pageIndex = pageNumber - 1
    offset = pageSize * pageIndex


    #totalCountSql = "SELECT COUNT(*) from `user_storybook_list` WHERE `userId`=%d" % userId
    totalCountOk=cursor.execute(sql)
    totalCount = totalCountOk
    if totalCount > 0:
        totalPageNum = int(totalCount / pageSize)
        if (totalCount % pageSize) > 0:
            totalPageNum += 1
    print('totalPageNum', totalPageNum)

        #if pageNumber > totalPageNum:
         #   return ( "Current page number %d exceed max page number %d" % (
          #      pageNumber, totalPageNum))

    sql_page = "select * from table_struct_schedule LIMIT %d OFFSET %d" % (pageSize, offset)
    totalCountOk = cursor.execute(sql_page)
    if totalCountOk:
        result = cursor.fetchall()
        pagenums = len(result)
        service_schedule = []
        for row in result:
            sid = row[0]
            IP = row[1]
            port = row[2]
            user = row[3]
            password = row[4]
            DBName = row[5]
            tableName = row[6]
            startTime = row[7]
            intervalTime = row[8]
            endTime = row[9]
            repeatTimes = row[10]
            enable = row[11]
            createTime = row[12]
            lastUpdate = row[13]

            d = {'scheduleID': sid, "IP": IP, "port": port, "user": user, "password": password,
                 "startTime": str(startTime),
                 'DBName': DBName, 'tableName': tableName,
                 "intervalTime": intervalTime,
                 "endTime": str(endTime), "repeatTimes": repeatTimes, "enable": enable,
                 "createTime": str(createTime), "lastUpdate": str(lastUpdate)}

            service_schedule.append(d)
        return_data = {

                "total_num": totalCount,
                "page_num": pageNumber,
                "page_size":pageSize,
                "num": pagenums,
                'service_schedules': service_schedule,
            }





        return_dict["data"] =return_data


    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接



    #return_dict=json.loads(json.dumps(return_dict), object_pairs_hook=OrderedDict)

    return jsonify(return_dict)


@app.route("/DBservice", methods=["GET"])
def check_DBservice():
    return_dict = {'rcode':'200','msg':'ok'}
    sql1=''
    sql2=''
    sql3=''
    sql4=''
    sql5=''

    # 判断传入的json数据是否为空
    #if request.get_data() is None:
     #   return_dict['status'] = 'error'
      #  return_dict['reason'] = '请求参数为空'
       # return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    getData = request.get_data()
    print('getdata',getData)
    # 传入的参数为bytes类型，需要转化成json
    if len(getData)!=0:
        get_Data = json.loads(getData)
        print('ok')
        print(get_Data)
        IP = get_Data.get('IP')
        if IP is not None:
            sql1 = ' hostIP = \'%s\'' % IP
        DBServiceType = get_Data.get('DBServiceType')
        if DBServiceType is not None:
            sql2 = ' service = \'%s\'' % DBServiceType
        port = get_Data.get('port')
        if port is not None:
            sql3 = ' port = \'%s\'' % port

        foundTimeRangeStart = get_Data.get('foundTimeRangeStart')
        if foundTimeRangeStart is not None:
            sql4 = ' foundTime > \'%s\'' % foundTimeRangeStart
        foundTimeRangeEnd = get_Data.get('foundTimeRangeEnd')
        if foundTimeRangeEnd is not None:
            sql5 = ' foundTime < \'%s\'' % foundTimeRangeEnd


    sqlx=[sql1,sql2,sql3,sql4,sql5]
    print(sqlx)

    # 默认返回内容
    #user_list = db.session.query(User).all()  # 查询所有。 query(User)表示查询所有列
    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()

    flag=0
    sql = 'select * from service_detection'
    for s in sqlx:
        if s!='':
            flag+=1
            if flag==1:
                sql=sql+' where'
            else:
                sql=sql+' and'
        sql=sql+s
    print(sql)

    pageSize = 10
    totalCount = -1
    totalPageNum = -1

    pageNumber = 1
    pageIndex = pageNumber - 1
    offset = pageSize * pageIndex


    #totalCountSql = "SELECT COUNT(*) from `user_storybook_list` WHERE `userId`=%d" % userId
    totalCountOk=cursor.execute(sql)
    totalCount = totalCountOk
    if totalCount > 0:
        totalPageNum = int(totalCount / pageSize)
        if (totalCount % pageSize) > 0:
            totalPageNum += 1


        #if pageNumber > totalPageNum:
         #   return ( "Current page number %d exceed max page number %d" % (
          #      pageNumber, totalPageNum))


    sql_page = sql+" LIMIT %d OFFSET %d" % (pageSize, offset)

    totalCountOk = cursor.execute(sql_page)
    if totalCountOk:
        result = cursor.fetchall()
        pagenums = len(result)
        service_detections = []
        for row in result:
            sid = row[0]
            service = row[1]
            version = row[2]
            hostIP = row[3]
            port = row[4]
            foundTime = row[6]

            d = {'scheduleID': sid, "IP": hostIP, "port": port, "version": version, "service": service,
                 "foundTime": str(foundTime)}

            service_detections.append(d)
        return_data = {

                "total_num": totalCount,
                "page_num": pageNumber,
                "num": pagenums,
                "page_size":pageSize,
                'service_detections': service_detections,
            }
        return_dict["data"] = return_data





    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接

    return jsonify(return_dict)

@app.route("/DBList", methods=["GET"])
def check_DBList():
    return_dict = {'rcode': '200', 'msg': 'ok'}
    sql1 = ''
    sql2 = ''
    sql3 = ''
    sql4 = ''
    sql5 = ''

    # 判断传入的json数据是否为空
    # if request.get_data() is None:
    #   return_dict['status'] = 'error'
    #  return_dict['reason'] = '请求参数为空'
    # return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    getData = request.get_data()
    print('getdata', getData)
    # 传入的参数为bytes类型，需要转化成json
    if len(getData) != 0:
        get_Data = json.loads(getData)
        print('ok')
        print(get_Data)
        IP = get_Data.get('IP')
        if IP is not None:
            sql1 = ' serviceIP = \'%s\'' % IP
        DBServiceType = get_Data.get('DBServiceType')
        if DBServiceType is not None:
            sql2 = ' DBServiceType = \'%s\'' % DBServiceType
        port = get_Data.get('port')
        if port is not None:
            sql3 = ' servicePort = \'%s\'' % port

        foundTimeRangeStart = get_Data.get('foundTimeRangeStart')
        if foundTimeRangeStart is not None:
            sql4 = ' foundTime > \'%s\'' % foundTimeRangeStart
        foundTimeRangeEnd = get_Data.get('foundTimeRangeEnd')
        if foundTimeRangeEnd is not None:
            sql5 = ' foundTime < \'%s\'' % foundTimeRangeEnd

    sqlx = [sql1, sql2, sql3, sql4, sql5]
    print(sqlx)

    # 默认返回内容
    # user_list = db.session.query(User).all()  # 查询所有。 query(User)表示查询所有列
    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()

    flag = 0
    sql = 'select * from db_tables'
    for s in sqlx:
        if s != '':
            flag += 1
            if flag == 1:
                sql = sql + ' where'
            else:
                sql = sql + ' and'
        sql = sql + s
    print(sql)

    pageSize = 10
    totalCount = -1
    totalPageNum = -1

    pageNumber = 1
    pageIndex = pageNumber - 1
    offset = pageSize * pageIndex

    # totalCountSql = "SELECT COUNT(*) from `user_storybook_list` WHERE `userId`=%d" % userId
    totalCountOk = cursor.execute(sql)
    totalCount = totalCountOk
    if totalCount > 0:
        totalPageNum = int(totalCount / pageSize)
        if (totalCount % pageSize) > 0:
            totalPageNum += 1
    #print('totalPageNum', totalPageNum)

    # if pageNumber > totalPageNum:
    #   return ( "Current page number %d exceed max page number %d" % (
    #      pageNumber, totalPageNum))

    sql_page = sql + " LIMIT %d OFFSET %d" % (pageSize, offset)
    #print("sql_page", sql_page)
    totalCountOk = cursor.execute(sql_page)
    if totalCountOk:
        result = cursor.fetchall()
        pagenums = len(result)
        print("pagenums", pagenums)
        service_detections = []
        for row in result:
            sid = row[0]
            serviceIP = row[1]
            servicePort = row[2]
            try:
                DBNames = json.loads(row[3])
            except:
                DBNames=row[3]
           # j = json.loads(DBNames)
            #print(j)

            foundTime = row[5]


            d = {'scheduleID': sid, "serviceIP": serviceIP, "servicePort": servicePort,"DBNames":DBNames,
                 "foundTime": str(foundTime)}

            service_detections.append(d)
        return_data = {

                "total_num": totalCount,
                "page_num": pageNumber,
                "num": pagenums,
                "page_size": pageSize,
                'DBlist': service_detections,
            }

        return_dict["data"] = return_data

    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接

    return jsonify(return_dict)
    # 默认返回内容
    #user_list = db.session.query(User).all()  # 查询所有。 query(User)表示查询所有列
    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    return_dict={"rcode":'200',"msg":"successful"}



    sql = 'select * from table_struct_schedule;'

    pageSize = 10
    totalCount = -1
    totalPageNum = -1

    pageNumber = 1
    pageIndex = pageNumber - 1
    offset = pageSize * pageIndex


    #totalCountSql = "SELECT COUNT(*) from `user_storybook_list` WHERE `userId`=%d" % userId
    totalCountOk=cursor.execute(sql)
    totalCount = totalCountOk
    if totalCount > 0:
        totalPageNum = int(totalCount / pageSize)
        if (totalCount % pageSize) > 0:
            totalPageNum += 1
    print('totalPageNum', totalPageNum)

        #if pageNumber > totalPageNum:
         #   return ( "Current page number %d exceed max page number %d" % (
          #      pageNumber, totalPageNum))


    data=[]
    for p in range(totalPageNum):

        sql_page = "select * from table_struct_schedule LIMIT %d OFFSET %d" % (pageSize, offset)
        totalCountOk = cursor.execute(sql_page)
        if totalCountOk:
            result = cursor.fetchall()
            pagenums=len(result)
            service_schedule = []
            for row in result:
                sid = row[0]
                IP = row[1]
                port = row[2]
                user = row[3]
                password = row[4]
                DBName = row[5]
                tableName = row[6]
                startTime = row[7]
                intervalTime = row[8]
                endTime = row[9]
                repeatTimes = row[10]
                enable = row[11]
                createTime = row[12]
                lastUpdate = row[13]

                d = {"scheduleID": sid, "IP": IP, "port": port,"user":user,"password":password,"startTime": str(startTime),
                     "DBName":DBName,"tableName":tableName,
                     "intervalTime": intervalTime,
                     "endTime": str(endTime), "repeatTimes": repeatTimes, "enable": enable,
                     "createTime": str(createTime), "lastUpdate": str(lastUpdate)}

                service_schedule.append(d)
            return_data = {

                    "total_num": totalCount,
                    "page_num": pageNumber,
                    "num": pagenums,
                    "service_schedules": service_schedule,
                }
            return_dict["data"]=return_data
            #data.append(return_data)

        pageNumber+=1
        pageIndex = pageNumber - 1
        offset = pageSize * pageIndex


    #return_dict["data"] =data


    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接



    #return_dict=json.loads(json.dumps(return_dict), object_pairs_hook=OrderedDict)

    return jsonify(return_dict)

@app.route("/tableList", methods=["GET"])
def check_tableList():
    return_dict = {'rcode':'200','msg':'ok'}
    sql1=''
    sql2=''
    sql3=''
    sql4=''
    sql5=''
    sql6=''
    # 判断传入的json数据是否为空
    #if request.get_data() is None:
     #   return_dict['status'] = 'error'
      #  return_dict['reason'] = '请求参数为空'
       # return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    getData = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    DBName=None
    if len(getData)!=0:
        get_Data = json.loads(getData)
        print('ok')
        print(get_Data)
        IP = get_Data.get('IP')
        if IP is not None:
            sql1 = ' serviceIP = \'%s\'' % IP
        DBServiceType = get_Data.get('DBServiceType')
        if DBServiceType is not None:
            sql2 = ' DBServiceType = \'%s\'' % DBServiceType
        port = get_Data.get('port')
        if port is not None:
            sql3 = ' servicePort = \'%s\'' % port

        foundTimeRangeStart = get_Data.get('foundTimeRangeStart')
        if foundTimeRangeStart is not None:
            sql4 = ' foundTime > \'%s\'' % foundTimeRangeStart
        foundTimeRangeEnd = get_Data.get('foundTimeRangeEnd')
        if foundTimeRangeEnd is not None:
            sql5 = ' foundTime < \'%s\'' % foundTimeRangeEnd
        DBName = get_Data.get('DBName')



    sqlx=[sql1,sql2,sql3,sql4,sql5]

    # 默认返回内容
    #user_list = db.session.query(User).all()  # 查询所有。 query(User)表示查询所有列
    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()

    flag=0
    sql = 'select * from db_tables'
    for s in sqlx:
        if s!='':
            flag+=1
            if flag==1:
                sql=sql+' where'
            else:
                sql=sql+' and'
        sql=sql+s

    pageSize = 10
    totalCount = -1
    totalPageNum = -1

    pageNumber = 1
    pageIndex = pageNumber - 1
    offset = pageSize * pageIndex


    #totalCountSql = "SELECT COUNT(*) from `user_storybook_list` WHERE `userId`=%d" % userId
    totalCountOk=cursor.execute(sql)
    totalCount = totalCountOk

    if totalCount > 0:
        totalPageNum = int(totalCount / pageSize)
        if (totalCount % pageSize) > 0:
            totalPageNum += 1


    # if pageNumber > totalPageNum:
    #   return ( "Current page number %d exceed max page number %d" % (
    #      pageNumber, totalPageNum))

    sql_page = sql + " LIMIT %d OFFSET %d" % (pageSize, offset)
    totalCountOk = cursor.execute(sql_page)
    return_data = {}
    if totalCountOk:
        result = cursor.fetchall()
        pagenums = len(result)
        service_detections = []
        for row in result:
            sid = row[0]
            serviceIP = row[1]
            servicePort = row[2]
            tableNames= json.loads(row[4])
            if DBName !=None:
                try:
                    tableNames=tableNames[DBName]
                except:
                    tableNames=[]
            foundTime = row[5]

            d = {'scheduleID': sid, "serviceIP": serviceIP, "servicePort": servicePort, "tableNames": tableNames,
                 "foundTime": str(foundTime)}

            service_detections.append(d)

        return_data = {

                "total_num": totalCount,
                "page_num": pageNumber,
                "num": pagenums,
                "page_size": pageSize,
                'tableList': service_detections,
            }
        return_dict["data"] = return_data

    #log.debug("%s -> %s, %s", totalCountSql, totalCountOk, resultDict)






    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接

    return jsonify(return_dict)

@app.route("/tableStruct", methods=["GET"])
def check_tableStruct():
    return_dict = {'rcode': '200', 'msg': 'ok'}
    sql1 = ''
    sql2 = ''
    sql3 = ''
    sql4 = ''
    sql5 = ''
    sql6 = ''
    sql7 = ''
    # 判断传入的json数据是否为空
    # if request.get_data() is None:
    #   return_dict['status'] = 'error'
    #  return_dict['reason'] = '请求参数为空'
    # return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    getData = request.get_data()
    print('getdata', getData)
    # 传入的参数为bytes类型，需要转化成json
    if len(getData) != 0:
        get_Data = json.loads(getData)
        print('ok')
        print(get_Data)
        IP = get_Data.get('IP')
        if IP is not None:
            sql1 = ' serviceIP = \'%s\'' % IP
        DBServiceType = get_Data.get('DBServiceType')
        if DBServiceType is not None:
            sql2 = ' DBServiceType = \'%s\'' % DBServiceType
        port = get_Data.get('port')
        if port is not None:
            sql3 = ' servicePort = \'%s\'' % port

        foundTimeRangeStart = get_Data.get('foundTimeRangeStart')
        if foundTimeRangeStart is not None:
            sql4 = ' foundTime > \'%s\'' % foundTimeRangeStart
        foundTimeRangeEnd = get_Data.get('foundTimeRangeEnd')
        if foundTimeRangeEnd is not None:
            sql5 = ' foundTime < \'%s\'' % foundTimeRangeEnd
        DBName = get_Data.get('DBName')
        if DBName is not None:
            sql6 = ' DBName = \'%s\'' % DBName
        tableName = get_Data.get('tableName')
        if tableName is not None:
            sql7 = ' tableName = \'%s\'' % tableName

    sqlx = [sql1, sql2, sql3, sql4, sql5, sql6,sql7]
    print(sqlx)

    # 默认返回内容
    # user_list = db.session.query(User).all()  # 查询所有。 query(User)表示查询所有列
    conn = pymysql.connect(host='140.143.218.23', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()

    flag = 0
    sql = 'select * from table_struct'
    for s in sqlx:
        if s != '':
            flag += 1
            if flag == 1:
                sql = sql + ' where'
            else:
                sql = sql + ' and'
        sql = sql + s
    print(sql)

    pageSize = 10
    totalCount = -1
    totalPageNum = -1

    pageNumber = 1
    pageIndex = pageNumber - 1
    offset = pageSize * pageIndex

    # totalCountSql = "SELECT COUNT(*) from `user_storybook_list` WHERE `userId`=%d" % userId
    totalCountOk = cursor.execute(sql)
    print(totalCountOk)
    #if totalCountOk:
       # resultDict = cursor.fetchall()
    totalCount = totalCountOk

    # log.debug("%s -> %s, %s", totalCountSql, totalCountOk, resultDict)

    if totalCount > 0:
        totalPageNum = int(totalCount / pageSize)
        if (totalCount % pageSize) > 0:
            totalPageNum += 1
    print('totalPageNum', totalPageNum)

    # if pageNumber > totalPageNum:
    #   return ( "Current page number %d exceed max page number %d" % (
    #      pageNumber, totalPageNum))

    sql_page = sql + " LIMIT %d OFFSET %d" % (pageSize, offset)
    print("sql_page", sql_page)
    totalCountOk = cursor.execute(sql_page)
    if totalCountOk:
        result = cursor.fetchall()
        pagenums = len(result)
        print("pagenums", pagenums)
        service_detections = []
        for row in result:
            sid = row[0]
            service = row[1]
            serviceIP = row[2]
            servicePort = row[3]
            DBName = row[4]
            tableName=row[5]
            try:
                tableStruct=json.loads(row[6])
            except:
                tableStruct=row[6]

            foundTime = row[7]

            d = {'scheduleID': sid, "serviceIP": serviceIP, "servicePort": servicePort, "DBName":DBName,"tableName":tableName,"tableStruct":tableStruct,
                 "foundTime": str(foundTime)}

            service_detections.append(d)
        return_data = {

                "total_num": totalCount,
                "page_num": pageNumber,
                "num": pagenums,
                "page_size": pageSize,
                'service_detections': service_detections,
            }
        return_dict["data"] = return_data



    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接

    return jsonify(return_dict)



handler =TimedRotatingFileHandler('logging.log', when='D')
#logging.FileHandler('D://flask.log', encoding='UTF-8')
handler.setLevel(logging.INFO)
app.logger.setLevel(logging.DEBUG)
logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s  - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)
app.logger.info('start')



if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host="0.0.0.0",port=800,debug=True)


