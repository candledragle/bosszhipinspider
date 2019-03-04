# coding:utf-8

import pymysql

if __name__ == '__main__':
    config = {
        'host': '172.16.2.128',
        'port': 3306,
        'user': 'sym',
        'passwd': '12345',
        'db': 'boss',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor
    }
    #打开数据库
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    result = cursor.execute("select version()")
    print (result)
    pass