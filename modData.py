import sys
import json
import sys
import appAuthentication
import random

#authenticated firebase and reddit api wrappers
fbase=appAuthentication.fbase
#reddit=appAuthentication.reddit

fbasePath='RedditScrape/'

metadata=fbase.get(fbasePath+'metadata/', None)
subreddits=metadata['subreddits']

def get_random_comments(numcomments):
	comments=[]
	posts=[]
	for sub in metadata['posts'].keys():
		for postID in metadata['posts'][sub].keys():
			posts.append(metadata['posts'][sub][postID])
	
	random.shuffle(posts)
	while len(comments)<numcomments and posts:
		post=posts.pop()
		#print(post['id'])
		postComments=fbase.get(fbasePath+'comments/'+post['id']+'/', None)
		for c in postComments:
			comments.append({'score': c[1], 'body': c[0], 'posttitle': post['title'], 'url': post['url'], 'subreddit': post['subreddit'], 'postID': post['id']})
	return comments

def up_or_down(numcomments):
	#Has this comment been upvoted or downvoted?
	comments=get_random_comments(numcomments)
	fbase.patch("/ModuleData/", {"UpDown": comments})

def comment_match(numcomments):
	#Match comment to correct subreddit out of 2 choices,
	#Then, match comment to correct title/url out of 2 choices
	comments=get_random_comments(numcomments)
	subredditPosts={}
	for subreddit in subreddits:
		subredditPosts[subreddit]=list(metadata['posts'][subreddit].values())
	for comment in comments:
		fakeSub=subreddits[random.randint(0, len(subreddits)-1)]
		while fakeSub==comment['subreddit']:
			fakeSub=subreddits[random.randint(0, len(subreddits)-1)]
		comment['fake_subreddit']=fakeSub
		posts=subredditPosts[comment['subreddit']]
		fakePost=posts[random.randint(0, len(posts)-1)]
		while fakePost['id']==comment['postID']:
				fakePost=posts[random.randint(0, len(posts)-1)]
		comment['fakeTitle']=fakePost['title']
		comment['fakeUrl']=fakePost['url']
	fbase.patch('/ModuleData/', {'CommentMatch': comments})

if __name__=='__main__':
	up_or_down(100)	
	comment_match(100)
