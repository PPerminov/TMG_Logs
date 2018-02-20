from configparser import ConfigParser as Config
from os import path


class config:
    def __init__(self, filename='config.ini'):
        self.configFile = filename
        if not path.isfile(self.configFile):
            self.configInput()
            self.createConfig()
            self.writeConfig()
        self.readConfig()

    def setParameter(self, param, value):
        exec('tmp=self.' + param)
        try:
            exec('self.' + param + '=' + value)
            return True
        except:
            exec('self.' + param + '=' + tmp)
            return False

    def readConfig(self):
        try:
            with open(self.configFile, 'r') as configFile:
                self.config.read(configFile)
            return True
        except:
            return False

    def writeConfig(self):
        with open(self.configfile, "w") as configFile:
            self.config.write(configFile)

    def setConfig(self):
        self.config = Config()
        self.config.add_section("DataBase")
        self.config.add_section("Source")
        self.config.add_section("Fields")
        self.config.set("DataBase", "address", self.address)
        self.config.set("DataBase", "database", self.database)
        self.config.set("DataBase", "password", self.password)
        self.config.set("DataBase", "user", self.user)
        self.config.set("Source", "source", self.source)

    def configInput(self):
        print('Please point mysql server for logging (if needed\
              - specify port after ":" )')
        server = input('Server: ')
        if ':' in server:
            server = server.split(':')
            self.port = server[1]
            self.address = server[0]
        else:
            self.port = 3306
            self.address = server
        print('Please point mysql database name (or use default "proxies")')
        self.database = input('Database: ')
        if not self.database:
            self.database = 'proxies'
        print('Please point mysql username (or use default "root")')
        self.username = input('Username: ')
        if not self.username:
            self.username = 'root'
        print('Please point mysql password')
        self.password = input('Password: ')
        print('Please point to folder with TMG logs')
        self.source = input('Source folder: ')
        self.proxyFields = ['c__ip', 'cs__username', 's__computername',
                            'r__host', 'r__ip', 'r__port', 'sc__bytes',
                            'cs__bytes', 'cs__transport', 'cs__uri',
                            'action', 'gmt__time']
        self.proxyFieldsFull = ['c__ip', 'cs__username', 'c__agent',
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
        # self.config.set(
        #     "Fields", "proxy", 'c__ip cs__username s__computername\
        #     r__host r__ip r__port sc__bytes cs__bytes cs__transport\
        #     cs__uri action gmt__time')
        # self.config.set(
        #     "Fields", "proxy_full", 'c__ip cs__username c__agent\
        #      sc__authenticated date time s__svcname s__computername\
        #      cs__referred r__host r__ip r__port time__taken sc__bytes\
        #      cs__bytes cs__protocol cs__transport s__operation cs__uri\
        #      cs__mime__type s__object__source sc__status s__cache__info\
        #      rule filterinfo cs__network sc__network error__info action\
        #      gmt__time authenticationserver nis__scan__result\
        #      nis__signature threatname malwareinspectionaction\
        #      malwareinspectionresult urlcategory\
        #      malwareinspectioncontentdeliverymethod mi__uagarrayid\
        #      sc__uagversion mi__uagmoduleid sc__uagid mi__uagseverity\
        #      mi__uagtype sc__uageventname mi__uagsessionid mi__uagtrunkname\
        #      mi__uagservicename sc__uagerrorcode malwareinspectionduration\
        #      malwareinspectionthreatlevel internal__service__info\
        #      nis__application__protocol nat__address\
        #      urlcategorizationreason sessiontype urldesthost\
        #      s__port softblockaction')
