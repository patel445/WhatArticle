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

fbasePath='RedditScrape/' #path in firebase to store data

metadata=fbase.get(fbasePath+'metadata/', None)
#print(metadata)
if not metadata:
	print("No metadata found. Exiting")
	sys.exit()
subreddits=metadata['subreddits']

if 'posts' in metadata.keys():
	posts=metadata['posts']
else:
	posts={}

def get_hot(subname, num_posts=20):
	subreddit=reddit.subreddit(subname)
	posts=subreddit.hot(limit=num_posts)
	return posts

def collect_submission_comments(post):
	post.comments.replace_more(limit=None)
	commentdata={}
	#commentdata['name']=submission.title
	#commentdata['url']=submission.url
	#commentdata['id']=submission.id
	#commentdata['datetime']=datetime.datetime.fromtimestamp(submission.created)
	comments=[]
	#commentdata['comments']=comments
	for c in post.comments:
		comments.append([c.body, c.score, c.id])
	return comments

def save_data(data):
	with open('commentdata/'+str(datetime.datetime.today())+'.json', 'w+') as file:
		json.dump(data, file)
	file.close()

def upload_data(data, path=fbasePath):
	result=fbase.patch(path, data)
	#print(result)	

def scrape_data(limit=3):
	#limit=number of submissions to get from each subreddit
	secondPass=[]
	for subname in subreddits:
		subreddit=reddit.subreddit(subname)
		if subname in posts.keys():
			postIDs=list(posts[subname].keys())
		else:
			postIDs=[]
		for post in subreddit.hot(limit=limit):
			postID=post.id
			if postID not in postIDs:
				postIDs.append(postID)
				postMeta={}
				postMeta['datetime']=datetime.datetime.fromtimestamp(post.created)		
				postMeta['title']=post.title
				postMeta['url']=post.url
				postMeta['subreddit']=subname
				postMeta['id']=postID
				comments=collect_submission_comments(post)
				upload_data({postID: postMeta}, path=fbasePath+'metadata/posts/'+subname+'/')
				upload_data({postID: comments}, path=fbasePath+'comments/')
			else:
				secondPass.append(post)
		for post in secondPass:
			comments=collect_submission_comments(post)
			upload_data({post.id: comments}, path=fbasePath+'comments/')
						
if __name__=='__main__':
	upload_data({'hello world': "hello firebase"}, path='/')
	scrape_data()
