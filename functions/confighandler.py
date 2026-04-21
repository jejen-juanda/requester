import os
import sys
from configparser import ConfigParser
from Globals import settings as st
class handler(ConfigParser):
	def __init__(self):
		ConfigParser.__init__(self)
		if not os.path.isfile("config.ini"):
			self["settings"] =st
			with open("config.ini","w") as config:
				self.write(config)
			print("A config file has been created, please fill in the necessary details before launching the program again. Exiting.")
			sys.exit()
	def request(self,info):
		self.read("config.ini")
		settings=self["settings"]
		return settings[info]