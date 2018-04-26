from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import utility
from utility import AppAuthentication
import string
import time
import numpy as np
import datetime
from multiprocessing import Process, Queue

#Processing module to parse the frequencies of words in subreddits and continuously update a wordcloud
#testing

#api authentication
reddit=AppAuthentication.reddit
fbase=AppAuthentication.fbase

sw=set(stopwords.words("english")) #stopwords to remove
#sw.extend(['would', 'I', "'"])
fbasePath="RedditScrape/"
metadata=fbase.get(fbasePath+'/metadata', None)
subreddits=metadata['subreddits']
#subs=reddit.subreddit("all+worldnews+") #looking through all subreddits to test
trantab=str.maketrans('', '', string.punctuation)

def comment_tokens(comment):
	comment=comment.translate(trantab)
	tokens=word_tokenize(comment)
	i=0
	numtokens=len(tokens)
	while i<numtokens:
			if tokens[i] in sw:
					tokens.pop(i)
					numtokens-=1
			else:
					i+=1
	return tokens
	
class CommentStreamer:
	#Class to stream comments based on subreddit input
	def __init__(self, subnames):
		self.subDict={}
		for subname in subnames:
			self.subDict[subname]=reddit.subreddit(subname)
	
	def get_comments(self, subname, numcomments, buff=100):
		comments=[]
		i=0
		for j in range(0, numcomments//buff):
			commentStream=self.subDict[subname].stream.comments()
			for c in commentStream:
				comments.append(c)
				i+=1
				if i%buff==0:
					break			
		return comments
	

class WordCloud:

	def __init__(self, subname):
		self.numCloudComments=1000 #the number of comments to consider at any given time
		self.cloudComments=[] #main data structure to hold comments.
		self.timeQueue=[] #keeping track the timestamps of comments being considered
		#subs=reddit.subreddit("+".join(subreddits))
		self.wordDict={}
		self.subname=subname
		procTime=[0]
		streamTime=[0]
		
	def add_comments(self, comments):
		#adding comments to cloudComments
		self.timeQueue.append(comments[0].created)
		newComments=[]
		for c in comments:
			newComments.append(comment_tokens(c.body))
		for comment in newComments:
			for word in comment:
				if word in self.wordDict.keys():
					self.wordDict[word]=self.wordDict[word]+1
				else:
					self.wordDict[word]=1
		self.cloudComments.extend(newComments)
		
	def remove_comments(self, numcomments):
		#Removing comments
		for i in range(0, numcomments):
			comment=self.cloudComments.pop(0)
			for word in comment:
				frequency=self.wordDict.pop(word, None)
				frequency-=1
				if frequency:
					self.wordDict[word]=frequency
		self.timeQueue.pop(0)
			
	def find_top_words(self, numcomments=10):
		#getting the top words in cloudComments using simple select algorithm
		def find_min(word_list):
			min=self.wordDict[word_list[0]]
			minWord=word_list[0]
			for word in word_list:
				if self.wordDict[word]<min:
					min=self.wordDict[word]
					minWord=word
			return min, minWord
		words=list(self.wordDict.keys())
		topWords=words[0:numcomments]
		min, minWord=find_min(topWords)
		for w in words:
			if self.wordDict[w]>min:
				topWords.remove(minWord)
				topWords.append(w)
				min, minWord=find_min(topWords)
		topWordDict={}
		for word in topWords:
			topWordDict[word]=self.wordDict[word]
		return topWordDict, self.timeQueue[-1]-self.timeQueue[0]
	
	
def save_wordcloud(worddict, timediff, label, info=[], path='wordclouds'):
	#putting word cloud in firebase
	timestring="Data recorded at "+str(datetime.datetime.now())+" over the course of "+str(int(timediff))+" seconds."
	info.append(timestring)
	for word in worddict.keys():
		info.append(str(word)+": "+str(worddict[word]))
	data={label: info}
	print(str(data))
	try:
		fbase.patch(path, data)
	except Exception as e:
		print("Firebase patch error")

		
def single_thread(subredditNames=subreddits):
	commentStreamer=CommentStreamer(subredditNames)
	wordClouds=[]
	for subname in subredditNames:
		wc=WordCloud(subname)
		wordClouds.append(wc)
		for i in range(0, 7):
			comments=commentStreamer.get_comments(subname, 100)
			wc.add_comments(comments)
		topWordDict, timediff=wc.find_top_words()
		save_wordcloud(topWordDict, timediff, subname, ['subreddit: '+subname])
	for i in range(0, 25):
		for wc in wordClouds:
			wc.remove_comments(100)
			comments=commentStreamer.get_comments(wc.subname, 100)
			wc.add_comments(comments)
			topWordDict, timediff=wc.find_top_words()
			print(str(topWordDict))
			save_wordcloud(topWordDict, timediff, wc.subname, ['subreddit: '+subname])
		
def multi_thread(num_threads=4):
	while True:
		processes=[]
		if num_threads>len(subreddits):
			num_threads=len(subreddits)
		i=0
		inc=len(subreddits)//num_threads
		j=inc
		while i<len(subreddits):
			p=Process(target=single_thread, args=(subreddits[i:i+inc],))
			processes.append(p)
			i=i+inc
			j=j+inc
		for p in processes:
			p.start()
		for p in processes:
			p.join()
			
def testTime(numcomments):
	
	def proc(subname, numc):
		sub=reddit.subreddit(subname)
		comments=[]
		i=0
		buff=100
		if buff>numc:
			buff=numc
		numloops=numc//buff
		for j in range(0, numloops):
			commentStream=sub.stream.comments()
			for c in commentStream:
				comments.append(c)
				i+=1
				if i%buff==0:
					break
			
	processes=[]
	sreddits=['worldnews', 'politics', 'news']
	numProcesses=len(sreddits)
	for s in sreddits:
		processes.append(Process(target=proc, args=(s, numcomments//len(sreddits),)))
	print("Using "+str(numProcesses)+" processes to get "+str(numcomments)+" comments")
	start=time.clock()
	for p in processes:
		p.start()
	for p in processes:
		p.join()
	end=time.clock()
	print("Time: "+str(end-start))
	print("Using a single process to get "+str(numcomments)+" comments.")
	start=time.clock()
	proc("+".join(sreddits), numcomments)
	end=time.clock()
	print("time: "+str(end-start))


def make_hot_wordclouds():
	all=reddit.subreddit('all')
	arrayData=[]
	label='hot_posts'
	
	for post in all.hot(limit=20):
		postMeta={}
		postMeta['datetime']=str(datetime.datetime.fromtimestamp(post.created))
		postMeta['title']=post.title
		postMeta['url']=post.url
		postMeta['id']=post.id
		post.comments.replace_more(limit=None)
		comments=[]
		for comment in post.comments:
			comments.append(comment)
		wc=WordCloud(None)
		postMeta['Number of comments']=len(comments)
		wc.add_comments(comments)
		topWordDict, timediff=wc.find_top_words()
		postMeta['top_words']=topWordDict
		postMeta['Subreddit']=post.subreddit.display_name
		arrayData.append(postMeta)
	#	postMeta['wordcloud']=topWordDict 
	fbase.patch('/', {'hot_posts': arrayData})
		
		
if __name__=='__main__':
	#multi_thread()
	make_hot_wordclouds()	
	
def stream_word_cloud():
	#streaming data to firebase
	#Final implementation should have infinite loop.
	for i in range(0, 5):
		add_comments(100)
	for i in range(0, 50):
		topWords=find_top_words()
		topWordDict={}
		for word in topWords:
			topWordDict[word]=wordDict[word]
		save_wordcloud(topWordDict, timeQueue[-1]-timeQueue[0])
		remove_comments(100)
		add_comments(100)
		
"""def test():
	#animating barchart
	for i in range(0, 5):
		add_comments(100)
		
	for i in range(0, 10):
		start=time.clock()
		topWords=find_top_words()
		for word in topWords:
			print(word+" "+str(wordDict[word]))
		remove_comments(100)
		add_comments(100)
		end=time.clock()
		print("Time: "+str(start-end))
	
	import matplotlib.pyplot as plt
	import matplotlib.animation as anim
	
	fig, ax=plt.subplots()
	yval=[]
	
	def update(i):
		remove_comments(100)
		add_comments(100)
		topWords=find_top_words()
		yval=[]
		ax.clear()
		ax.set_ylabel("frequency")
		ax.set_xlabel("word")
		ax.set_xticks(list(range(0, 10)))
		ax.set_xticklabels(topWords)
		print(str(topWords))
		for word in topWords:
			yval.append(wordDict[word])
	
		ax.set_ylim(0, min(yval)+max(yval))
		ax.bar(list(range(0, 10)), yval, 0.5, color='r')
		
	a=anim.FuncAnimation(fig, update, frames=None, repeat=False)
	plt.show()"""
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
						
						
