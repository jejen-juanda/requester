import os
class Requests():
	def __init__(self):
		if not os.path.isdir("requests"):
			os.mkdir("requests")
			os.mkdir("requests/channel-requests")
			os.mkdir("requests/user-account-requests")
		elif os.path.isdir("requests"):
			if not os.path.isdir("requests/channel-requests"):
				os.mkdir("requests/channel-requests")
			if not os.path.isdir("requests/user-account-requests"):
				os.mkdir("requests/user-account-requests")

		if not os.path.isdir("tracking"):
			os.mkdir("tracking")
			os.mkdir("tracking/channel-tracking")
			os.mkdir("tracking/user-account-tracking")
		elif os.path.isdir("tracking"):
			if not os.path.isdir("tracking/channel-tracking"):
				os.mkdir("tracking/channel-tracking")
			if not os.path.isdir("tracking/user-account-tracking"):
				os.mkdir("tracking/user-account-tracking")

	def count(self,path=""):
		number=0
		for each in os.listdir(path):
			number+=1
		return number