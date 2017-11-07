#!/usr/bin/env python3
from os.path import islink, realpath, abspath
from os import remove
# from datetime import datetime as dt
from time import time
from numpy import matrix
from re import search as res
import sqlite3
from pymysql import Connection as connection
from sys import exit
import passwd_local
import logging

db_file = 'prx.db'


def mysql_database():
    return connection(unix_socket='/var/run/mysqld/mysqld.sock', user=passwd_local.db_user, password=passwd_local.db_pass, db=passwd_local.db_name)


def mysq_recreate_tables(database):
    database_cursor = database.cursor()
    try:
        database_cursor.execute('drop table prx')
    except:
        print()
    try:
        database_cursor.execute('drop index prx_index on prx')
    except:
        print()
    database_cursor.execute(
        'CREATE TABLE IF NOT EXISTS prx(server VARCHAR(16), user VARCHAR(80), d_time DATETIME, source_ip VARCHAR(16), dest_ip VARCHAR(16), dest_port INT, recv INT,send INT, action VARCHAR(20), r_host TEXT, url TEXT)')
    database_cursor.execute(
        'CREATE INDEX prx_index ON prx (recv,user,source_ip)')
    database_cursor.close()
    database.commit()


def database_cursor(db_file):
    db = sqlite3.connect(db_file)
    create_table = "CREATE TABLE IF NOT EXISTS prx(server CHARACTER(15), USER CHARACTER, d_time INTEGER, source_ip CHARACTER(16), dest_ip CHARACTER(16), dest_port INTEGER, recv INTEGER,send INTEGER, action VARCHAR, r_host VARCHAR, url TEXT)"
    create_index = "CREATE INDEX IF NOT EXISTS prx_index ON prx (recv,user,r_host)"
    db.execute(create_table)
    db.execute(create_index)
    return db


folder = abspath('./LOGS')


def filelist(folder):
    from os import walk, path
    file_list = list()
    for root, subdirs, file_name in walk(path.abspath(folder)):
        if file_name:
            for fn in file_name:
                current_object = [root, fn]
                file_list.append(current_object)
    return file_list


def logs_parse(LOG, DB=None):
    DB_cur = DB.cursor()
    def parse(line):
        try:
            item = line.split('\t')
            client_time = (item[2] + " " + item[3])
            client_ip = item[0]
            client_username = item[1]
            server = item[4]
            r_ip = item[6]
            r_port = item[7]
            recv = item[8]
            send = item[9]
            proto = item[10]
            url = item[11]
            r_host = res(
                '^[htp]{0,4}[s]?[\:\/\/]{0,3}([\w\.\-]*)', url).groups()[0]
            status = item[13]
            return (server, client_username, client_time,
                    client_ip, r_ip, int(r_port), int(recv), int(send), status, r_host, url)
        except:
            print(line)

    lines_array = []
    t = time()
    with open(LOG, 'r') as log_file:
        bad_fields = ['#Date:', '#Software:', '#Fields:', '#Version:']
        while True:
            line = log_file.readline()
            if ('#Date:' in line) or ('#Software:' in line) or ('#Fields:' in line) or ('#Version:' in line):
                continue
            if (line == ''):
                break
            lines_array.append(line)
    print(time() - t, 'reading end')
    bd = []
    tmp_1 = 0
    t-time()
    for line in lines_array:
        tmp_1 += 1
        if tmp_1 == 5000:
            DB.commit()

            msg='5000 walked in '+str(time()-t)
            print(msg)
            logging.info(msg)
            tmp_1=1
            t=time()
        current_line = parse(line)
        DB_cur.execute(
            'insert into prx values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            current_line)
    t = time()
    DB.commit()
    DB_cur.close()


    print(time() - t, 'to commit to SQL')


logging.basicConfig(filename='current_' + str(time()) +
                    ".log", level=logging.DEBUG)
D1 = mysql_database()
mysq_recreate_tables(D1)

for filea in filelist(folder):
    # t = time()
    # print(t)
    logs_parse(filea[0] + "/" + filea[1], mysql_database())
D1.commit()
D1.close()
# print(time() - t)
# logs_parse('LOGS/ISALOG_20171005_WEB_000.w3c', mysql_database())

# logs_parse('log1',D1)
# exit()
