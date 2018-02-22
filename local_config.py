from configparser import ConfigParser as Config
from os import path
from getpass import getpass


def check_config(config,params):
    for param in params:
        if not config.get(param[0], param[1]):
            return False
    return True
def create_new_config(config_file,config):
    for section in sections:
        config.add_section(section)
    print('Please point mysql server for logging (if needed specify port after ":" )')
    server = input('Server: ')
    if ':' in server:
        server = server.split(':')
        config.set('DataBase', 'address', str(server[0]))
        config.set('DataBase', 'port', str(server[1]))
    else:
        config.set('DataBase', 'address', str(server))
        config.set('DataBase', 'port', '3306')
    print('Please point mysql database name (or use default "proxies")')
    database = input('Database: ')
    if not database:
        database = 'proxies'
    config.set('DataBase', 'database', str(database))
    print('Please point mysql username (or use default "root")')
    username = input('Username: ')
    if not username:
        username = 'root'
    config.set('DataBase', 'username', username)
    print('Please point mysql password')
    password = getpass('Password: ')
    config.set('DataBase', 'password', password)
    print('Please point to folder with TMG logs')
    source = input('Source folder: ')
    config.set('Source', 'source', source)
    proxy_fields = ['c__ip', 'cs__username', 's__computername',
                    'r__host', 'r__ip', 'r__port', 'sc__bytes',
                    'cs__bytes', 'cs__transport', 'cs__uri',
                    'action', 'time', 'date']
    config.set('Fields', 'proxy_fields', ' '.join(proxy_fields))
    proxy_fields_full = ['c__ip', 'cs__username', 'c__agent',
                         'sc__authenticated', 'date', 'time',
                         's__svcname', 's__computername',
                         'cs__referred', 'r__host', 'r__ip',
                         'r__port', 'time__taken', 'sc__bytes',
                         'cs__bytes', 'cs__protocol', 'cs__transport',
                         's__operation', 'cs__uri', 'cs__mime__type',
                         's__object__source', 'sc__status',
                         's__cache__info', 'rule', 'filterinfo',
                         'cs__network', 'sc__network', 'error__info',
                         'action', 'gmt__time', 'authenticationserver',
                         'nis__scan__result', 'nis__signature',
                         'threatname', 'malwareinspectionaction',
                         'malwareinspectionresult', 'urlcategory',
                         'malwareinspectioncontentdeliverymethod',
                         'mi__uagarrayid', 'sc__uagversion',
                         'mi__uagmoduleid', 'sc__uagid',
                         'mi__uagseverity', 'mi__uagtype',
                         'sc__uageventname', 'mi__uagsessionid',
                         'mi__uagtrunkname', 'mi__uagservicename',
                         'sc__uagerrorcode',
                         'malwareinspectionduration',
                         'malwareinspectionthreatlevel',
                         'internal__service__info',
                         'nis__application__protocol',
                         'nat__address', 'urlcategorizationreason',
                         'sessiontype', 'urldesthost', 's__port',
                         'softblockaction']
    config.set('Fields', 'proxy_fields_full', ' '.join(proxy_fields_full))
    with open(config_file, 'w') as config_file:
        config.write(config_file)





def config(config_file='config.ini'):
    config = Config()
    sections = ["DataBase", "Source", "Fields"]
    params = [[sections[1], 'source'],
              [sections[2], 'proxy_fields'],
              [sections[2], 'proxy_fields_full'],
              [sections[0], 'address'],
              [sections[0], 'port'],
              [sections[0], 'database'],
              [sections[0], 'username'],
              [sections[0], 'password']]
    if not path.isfile(config_file):
        create_new_config()
    else:
        config.read(config_file)
    if check_config():
        return config
    else:
        return
