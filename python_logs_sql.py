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

# recreate_tables(database().cursor())
#
# exit()


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


def prepare_log_from_file(log, database):
    database_cursor = database.cursor()

    def parse(line):
        bad_fields = ['#Date:', '#Software:', '#Fields:', '#Version:']
        for field in bad_fields:
            if field in line:
                return
        item = line.split('\n')[0].split('\t')
        date = list(map(lambda x: int(x), item[2].split('-')))
        time = list(map(lambda x: int(x), item[3].split(':')))
        client_ip = item[0]
        client_username = item[1]
        # client_time = dt(date[0], date[1], date[2],
        #                  time[0], time[1], time[2]).strftime('%s')
        client_time = (item[2] + " " + item[3])
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

    def check_lines(line_to_check):
        bad_fields = ['#Date:', '#Software:', '#Fields:', '#Version:']
        for field in bad_fields:
            if field in line_to_check:
                return False
        return True
    lines_counter = 0
    with open(log, 'r') as f:
        start_time = time()
        while True:
            lines_counter += 1
            line = f.readline()
            if line == '':
                break
            if check_lines(line) is True:
                current_line = parse(line)
                try:
                    database_cursor.execute(
                        'insert into prx values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', current_line)
                except:
                    logging.debug(current_line)
                if lines_counter % 100 == 0:
                    database.commit()
                    end_time = time()
                    delta_time = end_time - start_time
                    msg = '100 walked in ' + str(delta_time) + " seconds"
                    logging.info(msg)
                    start_time = time()

            else:
                continue

    # remove(log)
    database_cursor.close()
    database.commit()
    database.close()


mysq_recreate_tables(mysql_database())

logging.basicConfig(filename='current_' + str(time()) +
                    ".log", level=logging.DEBUG)

for filea in filelist(folder):
    # t = time()
    # print(t)
    prepare_log_from_file(filea[0] + "/" + filea[1], mysql_database())
    # print(time() - t)
