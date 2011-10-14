import os
import plistlib
import struct
import socket
from datetime import datetime
from progressbar import ProgressBar, Percentage, Bar, SimpleProgress, ETA

class DeviceInfo(dict):
	@staticmethod
	def create(dict):
		try:
			assert dict.has_key("dataVolumeUUID")
			filename = "%s.plist" % dict.get("dataVolumeUUID")
			return DeviceInfo(plistlib.readPlist(filename))
		except:
			return DeviceInfo(dict)

	def save(self):
		filename = "%s.plist" % self.get("dataVolumeUUID", "unk")
		print "Saving %s/%s" % (os.getcwd() , filename)
		plistlib.writePlist(self, filename)

	def __del__(self):
		pass#self.save()

class RamdiskToolClient(object):
	def __init__(self, host="localhost", port=1999):
		self.host = host
		self.port = port
		self.device_infos = {}
		self.connect()
		
	def connect(self):
		self.s = socket.socket()
		try:
			self.s.connect((self.host, self.port))
		except:
			raise Exception("Cannot cannot to ramdisk over usbmux, run \"python tcprelay.py -t 22:2222 1999:%d\"" % self.port)

	def getDeviceInfos(self):
		self.device_infos = self.send_req({"Request":"DeviceInfo"})
		print "Device UDID :", self.device_infos.get("udid")
		return DeviceInfo.create(self.device_infos)
	
	def downloadFile(self, path):
		res = self.send_req({"Request": "DownloadFile",
							  "Path": path})
		if type(res) == plistlib._InternalDict and res.has_key("Data"):
			return res["Data"].data

	def getSystemKeyBag(self):
		return self.send_req({"Request":"GetSystemKeyBag"})

	def bruteforceKeyBag(self, KeyBagKeys):
		return self.send_req({"Request":"BruteforceSystemKeyBag",
							"KeyBagKeys": plistlib.Data(KeyBagKeys)})
	
	def getEscrowRecord(self, hostID):
		return self.send_req({"Request":"GetEscrowRecord",
					  "HostID": hostID})
	
	def getPasscodeKey(self, keybagkeys, passcode):
		return self.send_req({"Request":"KeyBagGetPasscodeKey",
					  "KeyBagKeys": plistlib.Data(keybagkeys),
					  "passcode": passcode})
	
	def send_msg(self, dict):
		plist = plistlib.writePlistToString(dict)
		data = struct.pack("<L",len(plist)) + plist
		return self.s.send(data)
	
	def recv_msg(self):
		try:
			l = self.s.recv(4)
			ll = struct.unpack("<L",l)[0]
			data = ""
			l = 0
			while l < ll:
				x = self.s.recv(ll-l)
				if not x:
					return None
				data += x
				l += len(x)
			return plistlib.readPlistFromString(data)
		except:
			raise
			return None

	def send_req(self, dict):
		start = None
		self.send_msg(dict)
		while True:
			r = self.recv_msg()
			if type(r) == plistlib._InternalDict and r.get("MessageType") == "Progress":
				if not start:
					pbar = ProgressBar(r.get("Total",100),[SimpleProgress(), " ", Percentage(), " ", Bar()])
					pbar.start()
					start = datetime.utcnow()
				pbar.update( r.get("Progress", 0))
			else:
				if start:
					print dict.get("Request"), ":", datetime.utcnow() - start
				return r
