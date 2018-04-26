import firebase
from firebase.firebase import FirebaseAuthentication
from firebase.firebase import FirebaseApplication
import praw
import os.path


class AppAuthentication:

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

	
def longest_common_subsequence(pat1, pat2):

	seq=[]
	for i in range(0, len(pat1)+1):
		ar=[]
		for i in range(0, len(pat2)+1):
			ar.append("")
		seq.append(ar)
	flag=False	
	for i in range(1, len(pat1)+1):
		flag=False
		temp=seq[i-1][0]
		for j in range(1, len(pat2)+1):
			if(pat1[i-1]==pat2[j-1]):
				temp=seq[i-1][j-1]+pat1[i-1]
				flag=True
			if(flag and len(temp)>len(seq[i-1][j])):
				seq[i][j]=temp
			else:
				seq[i][j]=seq[i-1][j]
	#print(str(seq))
	return list(seq[len(pat1)][len(pat2)])
	
	
def process_comment(comment):
	import re
	from nltk.corpus import stopwords
	from nltk.tokenize import word_tokenize

	#https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
	comment=comment.lower()
	comment=re.sub(r'[^a-zA-Z ]', '', comment)
	word_tokens=word_tokenize(comment)
	filtered_comment = [w for w in word_tokens if not w in stop_words]
	comment=" ".join(filtered_comment)

	#comment=comment.replace("'", "")
	#comment=comment.replace(",", "")
	#comment=comment.replace(".", "")

	return comment

	
	
	
reddit=AppAuthentication.reddit
fbase=AppAuthentication.fbase
	
