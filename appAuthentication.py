import firebase
from firebase.firebase import FirebaseAuthentication
from firebase.firebase import FirebaseApplication
import praw
import os.path

if not os.path.isfile('firebaseauth.txt'):
	appLink=input("Input link to firebase: ")
	secret=input("Input secret key: ")
	user=input("Input user name or email: ")
	path=input("Input path in firebase to store comment data: ")
	with open("firebaseauth.txt", "w+") as file:
		file.write(secret+"\n")
		file.write(appLink+"\n")
		file.write(path+"\n")
		file.write(user+"\n")
	file.close()

else:
	with open("firebaseauth.txt", "r") as file:
		lines=file.readlines()
	file.close()
	secret=lines[0].replace("\n", "")
	appLink=lines[1].replace("\n", "")
	path=lines[2].replace("\n", "")
	user=lines[3].replace("\n", "")

auth=FirebaseAuthentication(secret, user)
fbase=FirebaseApplication(appLink, authentication=auth)
reddit=praw.Reddit(client_id='dZsi4V3pYz5jVw', client_secret=None, user_agent="Comment Comparison")
