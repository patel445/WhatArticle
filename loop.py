import wordCloud
import collectData
import modData
from multiprocessing import Process, Queue

#This is the primary file to call all data collection/parsing methods.
#The other files are somewhat a mess

def static_data_thread(i):
	while True:
		wordCloud.make_hot_wordclouds()
		#collectData.scrape_data(limit=10)
		modData.comment_match(100)
		modData.up_or_down(100)
	
p1=Process(target=wordCloud.multi_thread, args=(3,))
p2=Process(target=static_data_thread, args=(1,))

p1.start()
p2.start()
p1.join()
p2.join()
