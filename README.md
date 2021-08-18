# DB-Scanner
-------------
## 背景

![dbscan](C:\Users\fanyu\Downloads\image.png)
## 功能
api.py--提供http接口进行新增配置、配置更新、扫描结果读取  
dbscan.py--数据库和表扫描  
tablescan.py--表结构扫描

-----
## 环境
安装Python3.8.0（CentOS6）
```
#安装编译相关工具
yum -y groupinstall "Development tools"
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
yum install libffi-devel -y

#下载安装包解压
wget https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tar.xz
tar -xJvf Python-3.8.0.tar.xz

#编译安装
mkdir /usr/local/python3
cd Python-3.8.0
./configure --prefix=/usr/local/python3
make && make install

#创建软连接
ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3

#验证是否安装成功
python --version
pip3 --version
```
------------
安装nmap
```
yum install nmap
或rpm -vhU https://nmap.org/dist/nmap-7.80-1.x86_64.rpm
nmap -v
```
------
安装必要的包
```
pip3 install flask nmap logging pymysql json
```
## 使用
将mysql.lua放入usr/share/nmap/nselib
将mysqldatabase.nse、mysqldatabase2x.nse、mysqldatabase4x.nse放入usr/share/nmap/scripts/
```
python3 api.py 
python3 scan_engine.py
```
---
