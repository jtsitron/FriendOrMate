#! /usr/bin/env python

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import MySQLdb
import time
import json

config = utils.get_config('config.ini')
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
class listener(StreamListener):

    def on_data(self, data):
    	try:
            with open('England_new.json', 'a') as f:
            	f.write(data)
            	all_data = json.loads(data)
            	tweet = all_data["text"]
            	name = all_data["user"]["name"]
            	screen_name = all_data["user"]["screen_name"]
            	lang = all_data["user"]["lang"]
            	url = all_data["user"]["url"]
            	description = all_data["user"]["description"]
            	location = all_data["user"]["location"]
            	time_zone = all_data["user"]["time_zone"]
            	geo_enabled = all_data["user"]["geo_enabled"]
            	bb_coords_1 = all_data["place"]["bounding_box"]["coordinates"][0][0][0]
            	bb_coords_2 = all_data["place"]["bounding_box"]["coordinates"][0][0][1]
            	bb_coords_3 = all_data["place"]["bounding_box"]["coordinates"][0][1][0]
            	bb_coords_4 = all_data["place"]["bounding_box"]["coordinates"][0][1][1]
            	bb_coords_5 = all_data["place"]["bounding_box"]["coordinates"][0][2][0]
            	bb_coords_6 = all_data["place"]["bounding_box"]["coordinates"][0][2][1]
            	bb_coords_7 = all_data["place"]["bounding_box"]["coordinates"][0][3][0]
            	bb_coords_8 = all_data["place"]["bounding_box"]["coordinates"][0][3][1]
            	place_type = all_data["place"]["place_type"]
            	loc_name = all_data["place"]["name"]
            	loc_full_name = all_data["place"]["full_name"]
            	country_code = all_data["place"]["country_code"]
            	country = all_data["place"]["country"]
            	c.execute('SET NAMES utf8')
            	c.execute("INSERT INTO England (tweet, name, screen_name, lang, url, description, location, time_zone, place_type, loc_name, loc_full_name, country_code, country ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            		(tweet, name, screen_name, lang, url, description, location, time_zone, place_type, loc_name, loc_full_name, country_code, country))
            	conn.commit()

        #print((name,tweet))
        
        #return True
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))

    	

    def on_error(self, status):
        print status

        
 
    
     





twitterStream = Stream(auth, listener())
twitterStream.filter(locations=[-5.65625, 50.0213867188, 1.74658203125, 55.8079589844])
