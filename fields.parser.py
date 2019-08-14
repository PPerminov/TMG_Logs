from configparser import ConfigParser as Config
from time import time
from os import path
from os import walk
from multiprocessing import Pool as pool
from re import sub
from sys import exit
from getpass import getpass


class parser:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config()
        self.sql_id = self.sql()
        self.cursor_id = self.sql_id.cursor()
        self.sql_main = self.sql()
        self.cursor_main = self.sql_main.cursor()

    def config(self):
        self.config = Config()
        if not path.isfile(self.config_file):
            self.create_new_config()
        else:
            self.config.read(self.config_file)

    def create_new_config(self):
        # config = Config()
        params = {}
        params[server] = input('Mysql server: ')
        params[database] = input('Database name: ')
        params[username] = input('Username: ')
        params[password] = getpass('Password: ')
        params[source] = input('Logs folder: ')
        config.add_section('Main')
        for name, item in params.items():
            config.set('Main', name, item)
        with open(config_file, 'w') as config_file:
            config.write(config_file)
        self.config = config

    def sql(self):
        from pymysql import Connection as connection
        return connection(
            self.config.get('Main', 'address'),
            self.config.get('Main', 'username'),
            self.config.get('Main', 'password'),
            self.config.get('Main', 'database')
        )

    def id(self, data, table):
        cursor = self.cursor_id  # create cursor
        query = cursor.execute('select id from {table} where {table} = "{data}";'.format(
            table=table, data=data))  # check for data existence
        if query == 0:  # if not
            try:
                cursor.execute(
                    'insert into {table} ({table}) values ("{data}");')  # inserting data
                self.sql_id.commit()
                # cursor.commit()
            except:
                return False  # return False if failed
            return get_set_id(sql, data, table)  # return recursion for requery
        return query.fetchone()  # returning ID

    def get_data(self, string, fields, columns):
        data = {}
        for item in columns:
            data[item] = string[fields[item]]
        return data

    # face_main = get_data(string, fields, columns_main)
    # face_tabled = get_data(string, fields, columns_tabled)

    def create_query_data(sql, face_main, face_tabled, columns_main, columns_tabled):
        result_values = []
        for item in columns_main + columns_tabled:
            result_values.append()
        cursor = sql.cursor()


def parser(params):
    file1 = params['file1']
    config = params['config']
    proxy_fields = (config.get('Fields', 'proxy_fields')).split(' ')

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
    directory = path.realpath(config.get('Source', 'source'))
    all_list = walk(directory)
    for dirpath, dirnames, filenames in all_list:
        for fileitem in filenames:
            file_item = fileitem.lower()
            if 'isalog' in file_item and 'web' in file_item and 'w3c' in file_item:
                files.append({'file1': fileitem, 'config': config})
    f_pool = pool(2)
    f_pool.map(parser, files)
    f_pool.close()
    f_pool.join()


start()
