#! /usr/bin/env python
import tweepy
from tweepy import OAuthHandler
import MySQLdb
import utils
import sys
import argparse

def main(handle):
	parser = argparse.ArgumentParser(description='Fetch tweets for a given twitter account.')
	parser.add_argument('handle', metavar='handle', type=str, 
                   help='name of twitter account')
	args = parser.parse_args()

	config = utils.get_config('../config.ini')
	host = config['db']['host']
	user = config['db']['user']
	password = config['db']['password']
	db_name = config['db']['dbname']

	conn = MySQLdb.connect(host,user,password,db_name,charset='utf8',use_unicode=True)
	c = conn.cursor()

	consumer_key = config['twitter']['consumer_key']
	consumer_secret = config['twitter']['consumer_secret'] 
	access_token = config['twitter']['access_token']
	access_secret = config['twitter']['access_secret']

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	api = tweepy.API(auth)

	stuff = api.user_timeline(screen_name = handle, count = 8000, include_rts = False)
	
	for status in stuff:
	    tweet =status.text
	    screen_name = handle
	    c.execute("INSERT INTO tweets_by_user (HANDLE, TWEET) VALUES (%s,%s)",(screen_name, tweet))
	    conn.commit()    	

	conn.close()   

if __name__ == '__main__':
    main(sys.argv[1])         