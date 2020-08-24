#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask
from flask import request
import json
import nmap
import time, datetime
import pymysql
import logging
# 创建flask对象

from logging import handlers



#logging.debug('debug级别，一般用来打印一些调试信息，级别最低')
#logging.info('info级别，一般用来打印一些正常的操作信息')
#logging.warning('waring级别，一般用来打印警告信息')
#logging.error('error级别，一般用来打印一些错误信息')
#logging.critical('critical级别，一般用来打印一些致命的错误信息，等级最高')


logger = logging.getLogger('test')
logger.setLevel(level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
#stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler('t.log')
file_handler.setLevel(level=logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


logger.info("System Start")
app = Flask(__name__)
#logger.debug("Do something")
#logger.warning("Something maybe fail.")


#logger.debug('debug级别，一般用来打印一些调试信息，级别最低')
#logger.info('info级别，一般用来打印一些正常的操作信息')
#logger.warning('waring级别，一般用来打印警告信息')
#logger.error('error级别，一般用来打印一些错误信息')
#logger.critical('critical级别，一般用来打印一些致命的错误信息，等级最高')

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    filename='test3.log',
                    filemode='a'
                    )
logger.info('system start')
#time_rotating_file_handler = handlers.TimedRotatingFileHandler(filename='test3.log', when='S')
#time_rotating_file_handler.setLevel(logging.DEBUG)
#time_rotating_file_handler.setFormatter(formatter)

#logger.addHandler(time_rotating_file_handler)

@app.route("/config/update", methods=["POST"])
def check1():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    ConfigID = get_Data.get('ConfigID')
    #IPRange = get_Data.get('IPRange')
    serviceName = get_Data.get('serviceName')
    startTime = get_Data.get('startTime')
    intervalTime=get_Data.get('intervalTime')
    endTime = get_Data.get('endTime')
    repeatTimes = get_Data.get('repeatTimes')
    enable=get_Data.get('enable')
    configTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("""
           UPDATE schedule
           SET configTime=%s,serviceName=%s,startTime=%s,intervalTime=%s,endTime=%s,repeatTimes=%s,enable=%s
           WHERE id=%s
        """, (configTime, serviceName, startTime, intervalTime, endTime, repeatTimes, enable, ConfigID))
    conn.commit()  # 把修改的数据提交到数据库
    #logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        #level=logging.DEBUG)

    logger.info('Updating config information is completed。')


    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接
    # enable=get_Data.get('enable')
    # 对参数进行操作
    #print(startTime)

    #print('Program now starts on %s' % startTime)
    #print('Executing...')

    return_dict['configID']=ConfigID

    return_dict['result'] = tt2(ConfigID)


    return json.dumps(return_dict, ensure_ascii=False)


# 功能函数
def tt2(configID):
    # result_str = "%s今年%s岁" % (name, age)
    status="ok"

    return status,configID


@app.route("/config/add", methods=["POST"])
def check2():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    IPRange = get_Data.get('IPRange')
    serviceName = get_Data.get('serviceName')
    startTime = get_Data.get('startTime')
    intervalTime=get_Data.get('intervalTime')
    endTime = get_Data.get('endTime')
    repeatTimes = get_Data.get('repeatTimes')
    enable=get_Data.get('enable')
    configTime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    sql = "insert into schedule(configTime,IPRange,serviceName,startTime,intervalTime,endTime,repeatTimes,enable) VALUE (%s,%s,%s,%s,%s,%s,%s,%s);"

    cursor.execute(sql, (configTime,IPRange,serviceName,startTime,intervalTime,endTime,repeatTimes,enable))
    conn.commit()  # 把修改的数据提交到数据库
    logger.info('Adding config information is completed。')

    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接
    # enable=get_Data.get('enable')
    # 对参数进行操作

    #print('Program now starts on %s' % startTime)
    #Sprint('Executing...')

    return_dict['statu'] = tt1()



    return json.dumps(return_dict, ensure_ascii=False)


# 功能函数
def tt1():
    # result_str = "%s今年%s岁" % (name, age)
    status="ok"
    return status

@app.route("/read", methods=["POST"])
def check():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功'}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)

    serviceName = get_Data.get('serviceName')
    startTime = get_Data.get('startTime')
    endTime = get_Data.get('endTime')

    conn = pymysql.connect(host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')
    cursor = conn.cursor()
    sql = "select * from service_detection"
    cursor.execute(sql)
    r = cursor.fetchall()
    logger.info(r)

    #r=json.dumps(r)
    #r = json.loads(r)
    #print(json.dumps(result))
    return_dict['result']=str(r)
    logger.info('Read db is completed.')


    cursor.close()  # 关闭光标对象
    conn.close()  # 关闭数据库连接
    # enable=get_Data.get('enable')
    # 对参数进行操作





    return json.dumps(return_dict, ensure_ascii=False)


# 功能函数



if __name__ == "__main__":
    app.run(debug=True)

