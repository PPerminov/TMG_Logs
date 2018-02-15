from time import time
import multiprocessing as mp
import re
import sys
import variables
import cProfile

def parser(file1):
    def Fields_Parser(fields_line):
        array = (re.sub(r'-', '__', re.sub(r' ', '__',re.sub(r'^#fields: ', '', fields_line.lower().split("\n")[0])))).split('\t')
        position = 0
        for item in array:
            fields[item] = position
            position += 1
    def Sql():
        from pymysql import Connection as connection
        return connection(unix_socket='/var/run/mysqld/mysqld.sock', user=variables.db_user, password=variables.db_pass, db='proxies')
    sql = Sql()
    cursor = sql.cursor()
    tmp_lines = []
    counter=0
    t=time()
    with open(file1, 'r') as r:
        while True:
            try:
                x = (r.readline()).strip()
                if x == None:
                    sql.commit()
                    break
            except:
                break
            if x[0] == '#':
                if 'Fields' in x:
                    fields = {}
                    Fields_Parser(x)
                continue
            tm = {}
            tm_names = []
            tm_values = []
            line = x.split("\t")
            for field in variables.web_fields:
                tm_names.append(field)
                try:
                    position_t = fields[field]
                    result = re.sub(
                        r'"', "'", ('' if line[position_t] == "-" else line[position_t]))
                    tm_values.append(result)
                except:
                    tm_values.append('null')
            names = (', '.join(tm_names))
            values = (', '.join(list(map(lambda x: '"' + x + '"', tm_values))))
            qry = ("Insert Into tmp (%s) Values (%s)" % (names, values)).encode()
            cursor.execute(qry)

            counter+=1
            if counter % 100000 == 0:
                print(counter)
                sql.commit()
    # sql.commit()



if __name__ == '__main__':
    # logging.basicConfig(filename=abspath(variables.logs_folder) +
                        # '/current_' + str(time()) + ".log", level=logging.DEBUG)
    # try:
    #     DB = connect_database(sqlite="file.db")
    #     # mysq_recreate_tables(DB)
    #     # files = filelist(variables.source_folder)
    files = ['ISALOG_20180214_WEB_000.w3c','ISALOG_20180214_WEB_001.w3c']
    # print(files)
    f_pool = mp.Pool(2)
    f_pool.map(parser, files)
    f_pool.close()
    f_pool.join()
    # connect_database(DB)
    # except KeyboardInterrupt:
    #     killall()






# cProfile.run("parser()")
