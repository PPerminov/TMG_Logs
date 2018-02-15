#!/usr/bin/env python3
from os.path import islink, realpath, abspath
from os import remove
from time import time
from re import search as res
from sys import exit
import variables
import inspect
import logging
import multiprocessing as mp


# def FieldsParser(fields):
#     print()


def log(type, func_name, status, start_time, end_time=None, extra_msg=''):
    d1 = ' '
    d2 = ' - '
    if status == 'started':
        time_delta = str(start_time)
        atin = 'at'
    else:
        time_delta = str(end_time - start_time)
        atin = 'in'
    msg = func_name + d1 + status + d1 + atin + d1 + time_delta + d2 + extra_msg
    if type == 'debug':
        logging.debug(msg)
    elif type == 'info':
        logging.info(msg)
    else:
        return False
    return start_time


def connect_database(DB=None, sqlite=None):
    func_name = inspect.getframeinfo(inspect.currentframe()).function
    stime = log('info', func_name, 'started', time())
    if sqlite:
        # print(2131241)
        from sqlite3 import Connection
        DB = Connection(sqlite)
        log('info', func_name, 'close DB', stime, time())
        return DB
    if DB:
        DB.commit()
        DB.close()
        log('info', func_name, 'close DB', stime, time())
        return
    from pymysql import Connection as connection
    DB = connection(unix_socket='/var/run/mysqld/mysqld.sock',
                    user=variables.db_user, password=variables.db_pass, db=variables.db_name)
    log('info', func_name, 'started', time(), stime)
    return DB


def mysq_recreate_tables(database):
    func_name = inspect.getframeinfo(inspect.currentframe()).function
    stime = log('info', func_name, 'started', time())
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
    log('info', func_name, 'ended', stime, time())


def filelist(folder):
    func_name = inspect.getframeinfo(inspect.currentframe()).function
    stime = log('info', func_name, 'started', time())
    from os import walk, path
    file_list = list()
    for root, subdirs, file_name in walk(path.abspath(folder)):
        if file_name:
            for fn in file_name:
                file_list.append(root + "/" + fn)
    log('info', func_name, 'ended', stime, time())
    return file_list


def parse6(line):
 #   func_name = inspect.getframeinfo(inspect.currentframe()).function
    #    stime = log('info', func_name, 'started', time())
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
        logging.debug('Parse error: ' + line)


def logs_parse(LOG):
    func_name = inspect.getframeinfo(inspect.currentframe()).function
    stime = log('info', func_name, 'started', time(), extra_msg=LOG)
    DB_cur = DB.cursor()
    lines_array = list()
#    msg = 'File read and parse started - ' + LOG + ' - ' + str(starttime)
#    logging.info(msg)
    with open(LOG, 'r') as log_file:
        bad_fields = ['#Date:', '#Software:', '#Fields:', '#Version:']
        while True:
            line = log_file.readline()
            if ('#Date:' in line) or ('#Software:' in line) or ('#Fields:' in line) or ('#Version:' in line):
                continue
            if (line == ''):
                break
            lines_array.append(line)
    read_end = time()
    array1 = []
    for item in lines_array:
        array1.append(parse6(item))
 #   t = time()
    for item in array1:
        try:
            DB_cur.execute(
                'insert into prx values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', item)
        except:
            mapped = map(lambda x: str(x), item)
            logging.debug(''.join(mapped))

    end_time = time()
  #  print('commited in', end_time - t)
    log('info', func_name, 'ended', stime, end_time)
  #  logging.info('completed file ' + LOG + ' in ' +
    # str(end_time - starttime) + ' seconds')
    DB_cur.close()


def killall():
    global f_pool
    global DB
    f_pool.terminate()
    DB.close()
    exit()


if __name__ == '__main__':
    logging.basicConfig(filename=abspath(variables.logs_folder) +
                        '/current_' + str(time()) + ".log", level=logging.DEBUG)
    try:
        DB = connect_database(sqlite="file.db")
        # mysq_recreate_tables(DB)
        # files = filelist(variables.source_folder)
        files = ['LOGS/ISALOG_20170919_WEB_000.w3c']
        # print(files)
        f_pool = mp.Pool(1)
        f_pool.map(logs_parse, files)
        f_pool.close()
        f_pool.join()
        connect_database(DB)
    except KeyboardInterrupt:
        killall()
