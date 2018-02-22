from time import time
import multiprocessing as mp
import re
import sys
import os
import local_config

# class parser:
#     def __init__(self):


def parser(params):
    qry=''
    fooo=open('result.txt','w')
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
    with open(file1, 'r') as r:
        while True:
            t=time()
            try:
                x = (r.readline()).strip()
                if x is None or x == '':
                    sql.commit()
                    break
            except:
                break
            if x[0] == '#':
                if 'Fields' in x:
                    fields = {}
                    array = (re.sub(r'-', '__', re.sub(r' ', '__', re.sub(r'^#fields: ',
                                                                          '', x.lower().split("\n")[0])))).split('\t')
                    position = 0
                    for item in array:
                        fields[item] = position
                        position += 1
                continue
            tm = {}
            tm_names = []
            tm_values = []
            line = x.split("\t")
            for field in proxy_fields:

                try:

                    position_t = fields[field]
                    if line[position_t] == "-":
                        pass
                    else:
                        result = re.sub(r'\\', r'\\\\', re.sub(
                            r'"', "'", (line[position_t])))
                    tm_values.append('"' + result + '"')
                    tm_names.append(field)
                except:
                    pass
            names = (', '.join(tm_names))
            values = (', '.join(tm_values))
            qry = ("Insert Into tmp (%s) Values (%s);\n" %
                   (names, values)).encode()
            cursor.execute(qry)
            counter += 1
            ccg=100000
        # fooo.write(qry)
            if counter % ccg == 0:
                # print(counter)
                print('{0:.10f}'.format(((time()-t)/ccg)))
                sql.commit()


def start():
    files = []
    config = local_config.config()

    directory = os.path.realpath(config.get('Source', 'source'))
    # print(directory)
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
