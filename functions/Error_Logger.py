from datetime import datetime
import sys
#I'm too lazy to create a proper logging system, so this will do for now.
def log():
	date=datetime.now()
	now=date.strftime("%m/%d/%Y, %H:%M")
	file=open("Errors.log","a")
	file.write(now+"\n")
	sys.stderr=file
	file.write("\n")