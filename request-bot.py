import teamtalk
import os
import sys
import re
from functions import Error_Logger as logger
from functions.encryption import Encryption as enc
from functions.telegram import notifier
from functions import telegram_listener
from classes import handler,requests
from Globals import bantuan,admin,unrecognized,empty,success,syntax,details,exists,null,deleted,cleared,incorrect,id,cnotification,unotification,notifications
t=teamtalk.TeamTalkServer()
notifications=handler.request("NOTIFICATIONS")
@t.subscribe("messagedeliver")
def message(server,params):
	global notifications
	if params["type"] ==teamtalk.USER_MSG:
		content=params["content"]
		sender=t.get_user(params["srcuserid"])
		if content.startswith("bp"):
			raw = content[2:].strip().lstrip(",")

			info = [x.strip() for x in raw.split(",")]
			
			if len(info) < 2 or info[0] == "":
				server.user_message(sender,syntax)
			elif len(info) < 3:
				server.user_message(sender,details)
			else:

				teks_simpan = f"{info[0]},{info[1]},{info[2]}"
				
				if not os.path.isfile(f"requests/user-account-requests/{sender['nickname']}{'.request'}"):
					encoded = teks_simpan.encode()
					encrypted = enc.encrypt(encoded)
					with open(f"requests/user-account-requests/{sender['nickname']}.request", "wb") as request:
						request.write(encrypted)
					server.user_message(sender,success)
					
					if notifications:
						detail_pesan = (
							f"Request Akun Baru dari: {sender['nickname']}\n\n"
							f"Detail:\n"
							f"- Username: {info[0]}\n"
							f"- Password: {info[1]}\n"
							f"- Nama: {info[2]}"
						)
						notifier.sendMessage(id, detail_pesan)
				else:
					server.user_message(sender,exists)
		elif content.startswith("bc"):

			raw = content[2:].strip().lstrip(",")
			info = [x.strip() for x in raw.split(",")]
			
			if len(info) < 2 or info[0] == "":
				server.user_message(sender,incorrect)
			elif len(info) < 4:
				server.user_message(sender,details)
			else:
				teks_simpan = f"{info[0]},{info[1]},{info[2]},{info[3]}"
				
				if not os.path.isfile(f"requests/channel-requests/{sender['nickname']}{'.request'}"):
					encoded = teks_simpan.encode()
					encrypted = enc.encrypt(encoded)
					with open(f"requests/channel-requests/{sender['nickname']}.request", "wb") as request:
						request.write(encrypted)
					server.user_message(sender,success)
					
					if notifications:
						detail_pesan = (
							f"Request Channel Baru dari: {sender['nickname']}\n\n"
							f"Detail:\n"
							f"- Nama Channel: {info[0]}\n"
							f"- Password: {info[1]}\n"
							f"- Op Password: {info[2]}\n"
							f"- Topik: {info[3]}"
						)
						notifier.sendMessage(id, detail_pesan)
				else:
					server.user_message(sender,exists)
		elif content=="bantuan":
			server.user_message(sender,bantuan)
			if t.get_role(params["srcuserid"])=="admin":
				split=admin.split("\n")
				for i in split:
					server.user_message(sender,i)
		elif content=="check":
			if t.get_role(params["srcuserid"])=="admin":
				channels=requests.count("requests/channel-requests")
				users=requests.count("requests/user-account-requests")
				server.user_message(sender,f"There are {channels} channel requests, and {users} user requests")
			else:
				server.user_message(sender,unrecognized)
		elif content.startswith("see"):
			if t.get_role(params["srcuserid"])=="admin":
				parser=content.split()
				if len(parser)<2:
					server.user_message(sender,incorrect)
				elif parser[1]=="channel-requests":
					filelist=os.listdir("requests/channel-requests")
					if filelist!=[]:
						for i in filelist:
							nickname=os.path.splitext(i)
							server.user_message(sender,nickname[0])
					else:
						server.user_message(sender,empty)
				elif parser[1]=="user-account-requests":
					filelist=os.listdir("requests/user-account-requests")
					if filelist!=[]:
						for i in os.listdir("requests/user-account-requests"):
							nickname=os.path.splitext(i)
							server.user_message(sender,nickname[0])
					else:
						server.user_message(sender,empty)
			else:
				server.user_message(sender,unrecognized)
		elif content.startswith("remove"):
			if t.get_role(params["srcuserid"])=="admin":
				parser=content.split()
				if len(parser)<2:
					server.user_message(sender,incorrect)
				elif parser[1]=="channel-requests":
					if len(parser)==3:
						if os.path.isfile(f"requests/channel-requests/{parser[2]}.request"):
							os.remove(f"requests/channel-requests/{parser[2]}.request")
							server.user_message(sender,deleted)
						else:
							server.user_message(sender,null)
					else:
						name=""
						for i in parser[2:]:
							name+=f"{i} "
						nickname=name[len(name)-1].replace(" ","") +name[:len(name)-1]
						if os.path.isfile(f"requests/channel-requests/{nickname}.request"):
							os.remove(f"requests/channel-requests/{nickname}.request")
							server.user_message(sender,deleted)
						else:
							server.user_message(sender,null)
				elif parser[1]=="user-account-requests":
					if len(parser)==3:
						if os.path.isfile(f"requests/user-account-requests/{parser[2]}.request"):
							os.remove(f"requests/user-account-requests/{parser[2]}.request")
							server.user_message(sender,deleted)
						else:
							server.user_message(sender,null)
					else:
						name=""
						for i in parser[2:]:
							name+=f"{i} "
						nickname=name[len(name)-1].replace(" ","") +name[:len(name)-1]
						if os.path.isfile(f"requests/user-account-requests/{nickname}.request"):
							os.remove(f"requests/user-account-requests/{nickname}.request")
							server.user_message(sender,deleted)
						else:
							server.user_message(sender,null)
			else:
				server.user_message(sender,unrecognized)
		elif content.startswith("clear"):
			if t.get_role(params["srcuserid"])=="admin":
				parser=content.split()
				if len(parser)<2:
					server.user_message(sender,incorrect)
				elif parser[1]=="channel-requests":
					for file in os.listdir("requests/channel-requests"):
						os.remove(f"requests/channel-requests/{file}")
					server.user_message(sender,cleared)
				elif parser[1]=="user-account-requests":
					for file in os.listdir("requests/user-account-requests"):
						os.remove(f"requests/user-account-requests/{file}")
					server.user_message(sender,cleared)
				elif parser[1]=="all":
					for file in os.listdir("requests/channel-requests"):
						os.remove(f"requests/channel-requests/{file}")
					for file in os.listdir("requests/user-account-requests"):
						os.remove(f"requests/user-account-requests/{file}")
					server.user_message(sender,cleared)
			else:
				server.user_message(sender,unrecognized)
		elif content.startswith("creview"):
			if t.get_role(params["srcuserid"])=="admin":
				info=content.split()
				if len(info)<2:
					server.user_message(sender,incorrect)
				elif len(info)==2:
					try:
						with open(f"requests/channel-requests/{info[1]}{'.request'}","rb") as file:
							info=file.read()
						text=enc.decrypt(info).decode()
						info=text.split(",")
						server.user_message(sender,f"Channel name, {info[0]}. Password, {info[1]}. Operator password, {info[2]}. Topic, {info[3]}.")
					except FileNotFoundError:
						server.user_message(sender,null)
				else:
					name=""
					for i in info[1:]:
						name+=f"{i} "
					nickname=name[len(name)-1].replace(" ","") +name[:len(name)-1]
					try:
						with open(f"requests/channel-requests/{nickname}{'.request'}","rb") as file:
							info=file.read()
						text=enc.decrypt(info).decode()
						info=text.split(",")
						server.user_message(sender,f"Channel name, {info[0]}. Password, {info[1]}. Operator password, {info[2]}. Topic, {info[3]}.")
					except FileNotFoundError:
						server.user_message(sender,null)
			else:
				server.user_message(sender,unrecognized)
		elif content.startswith("ureview"):
			if t.get_role(params["srcuserid"])=="admin":
				info=content.split()
				if len(info)<2:
					server.user_message(sender,incorrect)
				elif len(info)==2:
					try:
						with open(f"requests/user-account-requests/{info[1]}{'.request'}","rb") as file:
							info=file.read()
						text=enc.decrypt(info).decode()
						info=text.split(",")
						server.user_message(sender,f"Username, {info[0]}. Password, {info[1]}. First name, {info[2]}.")
					except FileNotFoundError:
						server.user_message(sender,null)
				else:
					name=""
					for i in info[1:]:
						name+=f"{i} "
					nickname=name[len(name)-1].replace(" ","") +name[:len(name)-1]
					try:
						with open(f"requests/user-account-requests/{nickname}{'.request'}","rb") as file:
							info=file.read()
						text=enc.decrypt(info).decode()
						info=text.split(",")
						server.user_message(sender,f"Username, {info[0]}. Password, {info[1]}. First name, {info[2]}.")
					except FileNotFoundError:
						server.user_message(sender,null)
			else:
				server.user_message(sender,unrecognized)
		elif content=="notifications":
			if t.get_role(params["srcuserid"])=="admin":
				if notifications:
					notifications=False
					server.user_message(sender,"Notifications disabled")
				else:
					notifications=True
					server.user_message(sender,"Notifications enabled")
			else:
				server.user_message(sender,unrecognized)
		else:
			server.user_message(sender,unrecognized)
logger.log()
if __name__=="__main__":
	host=handler.request("HOST")
	port=handler.request("TCPPORT")
	username=handler.request("USERNAME")
	password=handler.request("PASSWORD")
	nickname=handler.request("NICKNAME")
	client=handler.request("CLIENT")
	notifications=handler.request("NOTIFICATIONS")
	telegram_listener.mulai_pendengar()
	t.set_connection_info(host,port)
	t.connect()
	t.login(nickname,username,password,client)
	t.join(1)
	t.handle_messages(1)