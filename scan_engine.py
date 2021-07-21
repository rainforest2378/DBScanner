
from queue import Queue
import pymysql
from concurrent.futures import ThreadPoolExecutor
import threading
import time
import dbscan
from dbutils.pooled_db import PooledDB



mysql_pool = PooledDB(pymysql, 15,host='cdb-faqfehvo.bj.tencentcdb.com', port=10172, user='fyl_chj_txmysql',
                           passwd='fyl@chjtxmysql', db='fyl', charset='utf8')  # 5为连接池里的最少连接数


# 查看future2代表的任务返回的结果


def p1():
#    print("Hello1")
    #print("当前时间戳是", time.time())
    conn = mysql_pool.connection()
    cursor = conn.cursor()
    #print('ok')
    sqli = "select * from service_schedule_I"
    sqlu = "select * from service_schedule_U"
    cursor.execute(sqli)
    result = cursor.fetchall()
    #print(result)

    tlist = []
    if len(result) != 0:
        for r in result:
            id = r[0]
            IPRange = r[1]
            DBServiceType = r[2]
            startTime = r[3]
            intervalTime = r[4]
            endTime = r[5]
            repeatTimes = r[6]
            enable = r[7]


            #scan = dbscan.service_scan_controller
            t1 =(IPRange, DBServiceType, startTime, intervalTime, endTime, repeatTimes, enable)

            tlist.append(t1)
            sqlid = 'delete from service_schedule_I where id=%s' % id
            # print(sqlid)
            cursor.execute(sqlid)
            conn.commit()
     #   print('complete')



    cursor.execute(sqlu)
    result = cursor.fetchall()
    #print(len(result))
    #print(result)
    for r in result:
        id = r[0]
        sid = r[1]
        IPRange = r[2]
        DBServiceType = r[3]
        startTime = r[4]
        intervalTime = r[5]
        endTime = r[6]
        repeatTimes = r[7]
        enable = r[8]


        #scan = dbscan.service_scan_controller
        t1 = (IPRange, DBServiceType, startTime, intervalTime, endTime, repeatTimes, enable)

        tlist.append(t1)
        sqlud = 'delete from service_schedule_U where id=%s' % id
        #print(sqlud)
        cursor.execute(sqlud)
        conn.commit()

    #print('complete')
    cursor.close()
    conn.close()


    return tlist

def p2():
    #print("Hello2")
    #print("当前时间戳是", time.time())
    conn = mysql_pool.connection()
    cursor = conn.cursor()
    sqli = "select * from db_tables_schedule_I;"
    sqlu = "select * from db_tables_schedule_U;"
    cursor.execute(sqli)
    result = cursor.fetchall()
    #print(result)

    tlist = []
    if len(result)!=0:
        for r in result:
            id = r[0]
            IP = r[1]
            port = r[2]
            user = r[3]
            password = r[4]
            startTime = r[5]
            intervalTime = r[6]
            endTime = r[7]
            repeatTimes = r[8]
            enable = r[9]

            #scan = dbscan.db_tables_scan_controller
            t1 = (IP, port, user, password, startTime, intervalTime, endTime, repeatTimes, enable)

            tlist.append(t1)
            sqlid = 'delete from db_tables_schedule_I where id=%s' % id
            cursor.execute(sqlid)
            conn.commit()

    cursor.execute(sqlu)
    result = cursor.fetchall()
    #print(result)
    for r in result:
        id = r[0]
        sid=r[1]
        IP = r[2]
        port = r[3]
        user = r[4]
        password = r[5]
        startTime = r[6]
        intervalTime = r[7]
        endTime = r[8]
        repeatTimes = r[9]
        enable = r[10]
        t1 = (IP, port, user, password, startTime, intervalTime, endTime, repeatTimes, enable)

        #scan = dbscan.db_tables_scan_controller


        tlist.append(t1)
        sqlud = 'delete from db_tables_schedule_U where id=%s' % id
        cursor.execute(sqlud)
        conn.commit()

        #print('subthread join')

    #print('complete')
    cursor.close()
    conn.close()
    #print(tlist)
    return tlist

def p3():
    #print("Hello3")
    #print("当前时间戳是", time.time())
    conn = mysql_pool.connection()
    cursor = conn.cursor()
    sqli = "select * from table_struct_schedule_I;"
    sqlu = "select * from table_struct_schedule_U;"
    cursor.execute(sqli)
    result = cursor.fetchall()
    #print(result)

    tlist = []
    if len(result)!=0:
        for r in result:
            id = r[0]
            IP = r[1]
            port = r[2]
            user = r[3]
            password = r[4]
            DBName=r[5]
            tableName=r[6]
            startTime = r[7]
            intervalTime = r[8]
            endTime = r[9]
            repeatTimes = r[10]
            enable = r[11]

            #scan = dbscan.db_tables_scan_controller
            t1 = (IP, port, user, password, DBName,tableName,startTime, intervalTime, endTime, repeatTimes, enable)
            #print(t1)
            tlist.append(t1)
            sqlid = 'delete from table_struct_schedule_I where id=%s' % id
            cursor.execute(sqlid)
            conn.commit()


    cursor.execute(sqlu)
    result = cursor.fetchall()
    for r in result:
        id = r[0]
        sid=r[1]
        IP = r[2]
        port = r[3]
        user = r[4]
        password = r[5]
        DBName=r[6]
        tableName=r[7]
        startTime = r[8]
        intervalTime = r[9]
        endTime = r[10]
        repeatTimes = r[11]
        enable = r[12]

        #scan = dbscan.table_struct_scan_controller
        t1 = (IP, port, user, password,DBName,tableName, startTime, intervalTime, endTime, repeatTimes, enable)

        tlist.append(t1)
        sqlud = 'delete from table_struct_schedule_U where id=%s' % id
        cursor.execute(sqlud)
        conn.commit()


    #print('complete')
    cursor.close()
    conn.close()
    return tlist

pool = ThreadPoolExecutor(max_workers=10)

class Scan:

    def __init__(self,func,second,action):#构造函数

        # 先进先出队列
        self.task_que = Queue(maxsize=10)
        self.func=func
        self.second=second
        self.action=action

    def loop_func(self):
        # 每隔second秒执行func函数
        while True:
            time.sleep(self.second)
            self.read_config_item()

    def read_config_item(self):
        #print('每隔几秒执行这个任务')
        par=self.func()
        #print('parameter',par)
        if(len(par)!=0):
            for p in par:
                self.task_que.put(p)
        #print("队列")
        #print(self.task_que.qsize())



    def run_dbscan(self):
        #print('--------')

        para_set=self.task_que.get()
        #print("参数")
        #print(para_set)
        #print(type(para_set))
        #pool.submit(self.action, lambda p: action(*p), para_set)
        pool.submit(lambda p: self.action(*p),para_set)
        #print("队列之后")
        #print(self.task_que.qsize())


if __name__ == '__main__':

    mus=[]
    second=5

    scan1= Scan(p1,second,dbscan.service_scan_controller)
    scan2 = Scan(p2,second,dbscan.db_tables_scan_controller)
    scan3 = Scan(p3,second,dbscan.table_struct_scan_controller)
    t1 = threading.Thread(target=scan1.loop_func)
    t2 = threading.Thread(target=scan2.loop_func)
    t3 = threading.Thread(target=scan3.loop_func)
    t1.start()
    t2.start()
    t3.start()


    mus.append(t1)
    mus.append(t2)
    mus.append(t3)

    while True:
        #print("jinruxunhuan")
        if scan1.task_que.empty() != True:
            #print('are you here1')
            scan1.run_dbscan()
        if scan2.task_que.empty() != True:
            #print('are you here2')
            scan2.run_dbscan()
        if scan3.task_que.empty()!=True:
            #print('are you here3')
            scan3.run_dbscan()
        #print("ruxunhuanzhihou")
