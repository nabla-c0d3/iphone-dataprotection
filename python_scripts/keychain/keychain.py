from crypto.aes import AESdecryptCBC
import struct
import sqlite3
import M2Crypto
from util import write_file
from util.bplist import BPlistReader
import plistlib
from util.cert import RSA_KEY_DER_to_PEM

def render_password(p):
    data = p["data"]
    if data != None and data.startswith("bplist") and data.find("\x00") != -1:
        pl = BPlistReader.plistWithString(p["data"])
        filename = "%s_%s_%d.plist" % (p["svce"],p["acct"],p["rowid"])
        plistlib.writePlist(pl, filename)
        write_file("bin_"+filename, p["data"])
        data = filename

    if p.has_key("srvr"):
        return "%s:%d;%s;%s" % (p["srvr"],p["port"],p["acct"],data)
    else:
        return "%s;%s;%s" % (p["svce"],p["acct"],data)

class Keychain:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.conn.row_factory = sqlite3.Row
        self.bsanitize = True

    def decrypt_data(self, data):
        return data #override this method

    def get_passwords(self):
        res = []
        for row in self.conn.execute("SELECT rowid, data, svce, acct, agrp FROM genp"):
            password = {}
            password["rowid"] = row["rowid"]
            password["svce"] = str(row["svce"])
            password["acct"] = str(row["acct"])
            password["data"] = self.decrypt_data(row["data"])
            password["agrp"] = str(row["agrp"])

            res.append(password)
        return res

    def get_inet_passwords(self):
        res = []
        for row in self.conn.execute("SELECT rowid, data, acct, srvr, port, agrp FROM inet"):
            password = {}
            password["rowid"] = row["rowid"]
            password["acct"] = str(row["acct"])
            password["srvr"] = str(row["srvr"])
            password["port"] = str(row["port"])
            password["data"] = self.decrypt_data(row["data"])
            password["agrp"] = str(row["agrp"])

            res.append(password)
        return res


    def get_certs(self):
        certs = {}
        pkeys = {}

        for row in self.conn.execute("SELECT cert.data, keys.data, cert.agrp FROM cert LEFT OUTER JOIN keys ON keys.klbl=cert.pkhh AND keys.agrp=cert.agrp"):
            cert_der = self.decrypt_data(row[0])
            #conn.execute("UPDATE cert SET data= WHERE rowid")

            cert = M2Crypto.X509.load_cert_der_string(cert_der)
            subject = cert.get_subject().as_text()
            subject = str(cert.get_subject().get_entries_by_nid(M2Crypto.X509.X509_Name.nid['CN'])[0].get_data())
            certs[subject+ "_%s" % row[2]] = cert

            if row[1]:
                pkey_der = self.decrypt_data(row[1])
                pkey_der = RSA_KEY_DER_to_PEM(pkey_der)
                pkeys[subject + "_%s" % row[2]] = pkey_der

        return certs, pkeys


    def save_passwords(self):
        passwords = "\n".join(map(render_password,  self.get_passwords()))
        inetpasswords = "\n".join(map(render_password,  self.get_inet_passwords()))
        write_file("keychain.csv", "Passwords\n"+passwords+"\nInternet passwords\n"+ inetpasswords)

    def save_certs_keys(self):
        certs, pkeys = self.get_certs()
        for c in certs:
            filename = (c)
            certs[c].save_pem(filename + ".crt")
        for k in pkeys:
            filename = (k)
            write_file(filename + ".key", pkeys[k])

    def sanitize(self, pw):
        if pw.startswith("bplist"):
            return "<binary plist data>"
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
            print "Account :\t" + p["acct"]
            print "Password :\t" + self.sanitize(p["data"])
            print "Agrp :\t" + p["agrp"]
            print "-"*60

        for p in self.get_inet_passwords():
            print "Server : \t" + p["srvr"] + ":" + p["port"]
            print "Account : \t" + p["acct"]
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
        for row in self.conn.execute("SELECT data FROM genp WHERE svce='push.apple.com'"):
            return self.decrypt_data(row["data"])
    
    def get_managed_configuration(self):
        for row in self.conn.execute("SELECT data FROM genp WHERE acct='Private' AND svce='com.apple.managedconfiguration' AND agrp='apple'"):
            return BPlistReader.plistWithString(self.decrypt_data(row["data"]))