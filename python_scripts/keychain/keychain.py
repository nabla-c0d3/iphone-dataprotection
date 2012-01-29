from store import PlistKeychain, SQLiteKeychain
from util import write_file
from util.bplist import BPlistReader
from util.cert import RSA_KEY_DER_to_PEM
import M2Crypto
import hashlib
import plistlib
import sqlite3
import string

printset = set(string.printable)

def render_password(p):
    data = p["data"]
    if data != None and data.startswith("bplist") and data.find("\x00") != -1:
        pl = BPlistReader.plistWithString(p["data"])
        filename = "%s_%s_%d.plist" % (p["svce"],p["acct"],p["rowid"])
        plistlib.writePlist(pl, filename)
        #write_file("bin_"+filename, p["data"])
        data = filename

    if p.has_key("srvr"):
        return "%s:%d;%s;%s" % (p["srvr"],p["port"],p["acct"],data)
    else:
        return "%s;%s;%s" % (p["svce"],p["acct"],data)

class Keychain(object):
    def __init__(self, filename):
        magic = open(filename, "rb").read(16)
        if magic.startswith("SQLite"):
            self.store = SQLiteKeychain(filename)
        elif magic.startswith("bplist"):
            self.store = PlistKeychain(filename)
        else:
            raise Exception("Unknown keychain format for %s" % filename)
        self.bsanitize = True
        self.items = {"genp": None, "inet": None, "cert": None, "keys": None}
        
    def decrypt_data(self, data):
        return data #override this method

    def decrypt_item(self, res):
        res["data"] = self.decrypt_data(res["data"])
        if not res["data"]:
            return {}             
        return res

    def get_items(self, table):
        if self.items[table]:
            return self.items[table]
        self.items[table] = filter(lambda x:x!={}, map(self.decrypt_item, self.store.get_items(table)))
        return self.items[table]

    def get_passwords(self):
        return self.get_items("genp")

    def get_inet_passwords(self):
        return self.get_items("inet")

    def get_keys(self):
        return self.get_items("keys")

    def get_cert(self):
        return self.get_items("cert")

    def get_certs(self):
        certs = {}
        pkeys = {}
        keys = self.get_keys()
        for row in self.get_cert():
            cert = M2Crypto.X509.load_cert_der_string(row["data"])
            subject = cert.get_subject().as_text()
            common_name = cert.get_subject().get_entries_by_nid(M2Crypto.X509.X509_Name.nid['CN'])
            if len(common_name):
                subject = str(common_name[0].get_data())
            else:
                subject = "cn_unknown_%d" % row["rowid"]
            certs[subject+ "_%s" % row["agrp"]] = cert
            
            for k in keys:
                if k["agrp"] == row["agrp"] and k["klbl"] == row["pkhh"]:
                    pkey_der = k["data"]
                    pkey_der = RSA_KEY_DER_to_PEM(pkey_der)
                    pkeys[subject + "_%s" % row["agrp"]] = pkey_der
                    break

        return certs, pkeys


    def save_passwords(self):
        passwords = "\n".join(map(render_password,  self.get_passwords()))
        inetpasswords = "\n".join(map(render_password,  self.get_inet_passwords()))
        print "Writing passwords to keychain.csv"
        write_file("keychain.csv", "Passwords;;\n"+passwords+"\nInternet passwords;;\n"+ inetpasswords)

    def save_certs_keys(self):
        certs, pkeys = self.get_certs()
        for c in certs:
            filename = c + ".crt"
            print "Saving certificate %s" % filename
            certs[c].save_pem(filename)
        for k in pkeys:
            filename = k + ".key"
            print "Saving key %s" % filename
            write_file(filename, pkeys[k])

    def sanitize(self, pw):
        if pw.startswith("bplist"):
            return "<binary plist data>"
        elif not set(pw).issubset(printset):
            pw = "<binary data> : " + pw.encode("hex")
        if self.bsanitize:
            return pw[:2] + ("*" * (len(pw) - 2))
        return pw

    def print_all(self, sanitize=True):
        self.bsanitize = sanitize
        print "-"*60
        print " " * 20 + "Passwords"
        print "-"*60

        for p in self.get_passwords():
            print "Service :\t" + p["svce"]
            print "Account :\t" + str(p["acct"])
            print "Password :\t" + self.sanitize(p["data"])
            print "Agrp :\t" + p["agrp"]
            print "-"*60

        for p in self.get_inet_passwords():
            print "Server : \t" + p["srvr"] + ":" + str(p["port"])
            print "Account : \t" + str(p["acct"])
            print "Password : \t" + self.sanitize(p["data"])
            print "-"*60

        certs, pkeys = self.get_certs()

        print " " * 20 + "Certificates"
        print "-"*60
        for c in sorted(certs.keys()):
            print c

        print "-"*60
        print " " * 20 + "Private keys"

        for k in sorted(pkeys.keys()):
            print k
        print "-"*60

    def get_push_token(self):
        for p in self.get_passwords():
            if p["svce"] == "push.apple.com":
                return p["data"]
    
    def get_managed_configuration(self):
        for p in self.get_passwords():
            if p["acct"] == "Private" and p["svce"] == "com.apple.managedconfiguration" and p["agrp"] == "apple":
                return BPlistReader.plistWithString(p["data"])
    
    def _diff(self, older, res, func, key):
        res.setdefault(key, []) 
        current = func(self)  
        for p in func(older):
            if not p in current and not p in res[key]:
                res[key].append(p)

    def diff(self, older, res):
        self._diff(older, res, Keychain.get_passwords, "genp")
        self._diff(older, res, Keychain.get_inet_passwords, "inet")
        self._diff(older, res, Keychain.get_cert, "cert")
        self._diff(older, res, Keychain.get_keys, "keys")
