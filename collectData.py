import sys
import time
import json
import datetime
import os
import sys
import datetime
import appAuthentication #module in system path

#authenticated firebase and reddit api wrappers
fbase=appAuthentication.fbase
reddit=appAuthentication.reddit

fbasePath='/' #path in firebase to store data

if not os.path.isfile('subreddits.txt'):
	print("Need to specify subreddit names on individual lines in file 'subreddits.txt'")
	sys.exit()

submissionIds=[]
submissions=fbase.get(fbasePath+'submissions/', None)
if submissions:
	submissionIds=list(submissions.keys())
else:
	submissions={}

subreddits=fbase.get(fbasePath+'subreddits/', None)
if not subreddits:
	print("No subreddits in firebase. Exiting")
	sys.exit()
print(str(subreddits))

def get_hot(subname, num_posts=20):
	subreddit=reddit.subreddit(subname)
	submissions=subreddit.hot(limit=num_posts)
	return submissions

def get_collected_ids(path=fbasePath+'collected_ids'):
	result=fbase.get(path, None)
	return result

def collect_submission_comments(submission):
	submission.comments.replace_more(limit=None)
	commentdata={}
	#commentdata['name']=submission.title
	#commentdata['url']=submission.url
	#commentdata['id']=submission.id
	#commentdata['datetime']=datetime.datetime.fromtimestamp(submission.created)
	comments=[]
	#commentdata['comments']=comments
	for c in submission.comments:
		comments.append([c.body, c.score])
	return comments

def save_data(data):
	with open('commentdata/'+str(datetime.datetime.today())+'.json', 'w+') as file:
		json.dump(data, file)
	file.close()

def upload_data(data, path=fbasePath):
	result=fbase.patch(path, data)
	print(result)	

def scrape_data(limit=10):
	#limit=number of submissions to get from each subreddit
	for subname in subreddits:
		subreddit=reddit.subreddit(subname)
		for submission in subreddit.hot(limit=limit):
			subID=submission.id
			if subID not in submissionIds:
				submissionIds.append(subID)
				subMeta={}
				subMeta['datetime']=datetime.datetime.fromtimestamp(submission.created)		
				subMeta['title']=submission.title
				subMeta['url']=submission.url
				subMeta['subreddit']=subname
				comments=collect_submission_comments(submission)
				upload_data({subID: subMeta}, path=fbasePath+'submissions/')
				upload_data({subID: comments}, path=fbasePath+'comments/')
						
if __name__=='__main__':
	upload_data({'hello world': "hello firebase"}, path='/')
	scrape_data()
