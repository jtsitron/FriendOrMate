#! /usr/bin/env python

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import MySQLdb
import time
import json
#from httplib.client import IncompleteRead


conn = MySQLdb.connect("127.0.0.1","username","password","dbname",charset='utf8',use_unicode=True)

c = conn.cursor()


#consumer key, consumer secret, access token, access secret.
consumer_key = 'blah'
consumer_secret = 'blah' 
access_token = 'blah'
access_secret = 'blah'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

class listener(StreamListener):

    def on_data(self, data):
    	try:
            with open('US_test.json', 'a') as f:
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
            	c.execute("INSERT INTO America_test (tweet, name, screen_name, lang, url, description, location, time_zone, place_type, loc_name, loc_full_name, country_code, country ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            		(tweet, name, screen_name, lang, url, description, location, time_zone, place_type, loc_name, loc_full_name, country_code, country))
            	conn.commit()
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))

    	

    def on_error(self, status):
        print status

        
 
    
     


while True:
    try:
        twitterStream = Stream(auth, listener())
        twitterStream.filter(locations=[-124.709960938, 24.5423339844, -66.9870117187, 49.3696777344])
    except IncompleteRead:
        continue
    except KeyboardInterrupt:
        stream.disconnect()
        break

conn.close()
