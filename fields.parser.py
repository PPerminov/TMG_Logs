from time import time
import multiprocessing as mp
import re
import sys
import os
import local_config


def parser(params):
    file1 = params['file1']
    config = params['config']
    proxy_fields = (config.get('Fields', 'proxy_fields')).split(' ')

    def sql(type='local', address='localhost', username='root', password=None, database='proxies'):
        from pymysql import Connection as connection
        if type != 'local':
            return connection(host=address, user=username, password=password, db=database)
        return connection(unix_socket=address, user=username, password=password, db=database)
    sql = sql(type=1, address=config.get('DataBase', 'address'), username=config.get('DataBase', 'username'),
              password=config.get('DataBase', 'password'), database=config.get('DataBase', 'database'))
    cursor = sql.cursor()
    tmp_lines = []
    counter = 0
    t = time()
    values = []
    with open(file1, 'r') as r:
        while True:
            t = time()
            try:
                x = (r.readline()).strip()
                if x is None or x == '':
                    cursor.executemany(current_query, values)
                    break
            except:
                sql.commit()
                break
            if x[0] == '#':
                if 'Fields' in x:
                    try:
                        cursor.executemany(current_query, values)
                        values = []
                    except:
                        print('!!!')
                    fields = {}
                    fields_array = (re.sub(r'-', '__', re.sub(r' ', '__', re.sub(r'^#fields: ',
                                                                                 '', x.lower().split("\n")[0])))).split('\t')
                    position = 0
                    for item in fields_array:
                        fields[item] = position
                        position += 1
                    marks = ','.join(['%s' for _ in fields_array])
                    names = ','.join(fields_array)
                    current_query = 'insert into tmp (' + \
                        names + ') values (' + marks + ');'
                continue
            tm_values = []
            line = x.split("\t")
            for field in fields_array:
                position_t = fields[field]
                data = line[position_t]
                try:
                    if data != '-':
                        result = re.sub(r'\\', r'\\\\', re.sub(
                            r'"', "'", (data)))
                    else:
                        result = 'null'
                    tm_values.append(result.encode())
                except:
                    pass
            values.append(tuple(tm_values))
            counter += 1
            ccg = 10000
            if counter % ccg == 0:
                cursor.executemany(current_query, values)
                values = []

                print('{0:.10f}'.format(((time() - t) / ccg)))
                sql.commit()
    sql.commit()


def start():
    files = []
    config = local_config.config()
    directory = os.path.realpath(config.get('Source', 'source'))
    all_list = os.walk(directory)
    for dirpath, dirnames, filenames in all_list:
        for fileitem in filenames:
            file_item = fileitem.lower()
            if 'isalog' in file_item and 'web' in file_item and 'w3c' in file_item:
                files.append({'file1': fileitem, 'config': config})
    f_pool = mp.Pool(2)
    f_pool.map(parser, files)
    f_pool.close()
    f_pool.join()


start()
