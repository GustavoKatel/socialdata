#!/usr/bin/python

import sys, os
import csv, json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

consumer_key=""
consumer_secret=""

access_token=""
access_token_secret=""

class CSVListener(StreamListener):

	def __init__(self, csvfile):
		self.csv = csv.writer(open(csvfile, "w"), delimiter=";")
		self.csv.writerow(["date", "id", "text", "retweets", "favorites"])
		self.size=0

	def on_data(self, data):
		obj = json.loads(data)
		self.csv.writerow([ obj["created_at"], obj["id"], obj["text"].encode("utf-8"), obj["retweet_count"], obj["favorite_count"] ])
		self.size+=1
		print "Size: ",self.size
		return True

	def on_error(self, status):
		print status

if __name__ == '__main__':
	if len(sys.argv)!=3:
		print "./socialdata_twitter.py query.txt out.csv"
		sys.exit(1)
	l = CSVListener(sys.argv[2])
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	# read query file
	f = open(sys.argv[1], "r")
	query = []
	for line in f:
		line=line.replace("\n", "")
		query.append(line)

	stream = Stream(auth, l)
	stream.filter(track=query)
