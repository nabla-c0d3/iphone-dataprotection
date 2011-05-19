from keychain4 import Keychain4
from util.bplist import BPlistReader

class KeychainBackup4(Keychain4):
    def __init__(self, filename, keybag):
        self.keychain = BPlistReader.plistWithFile(filename)
        self.keybag = keybag

    def get_passwords(self):
        res = []

        genps = self.keychain['genp']
        for genp in genps:
            password = {}
            password['svce'] = genp['svce']
            password['acct'] = genp['acct']
            password['agrp'] = genp['agrp']
            password['data'] = self.decrypt_data(genp['v_Data'].data)
            res.append(password)
        return res

    def get_inet_passwords(self):
        res = []

        inets = self.keychain['inet']
        for inet in inets:
            password = {}
            password['acct'] = inet['acct']
            password['srvr'] = inet['srvr']
            password['port'] = inet['port']
            password['data'] = self.decrypt_data(inet['v_Data'].data)
            password['agrp'] = inet['agrp']
            res.append(password)
        return res
