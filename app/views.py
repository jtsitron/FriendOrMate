from flask_app import app
from flask import render_template, request
import pymysql as mdb
import utils
from sklearn.externals import joblib
import numpy as np

from a_Model_old import ModelIt


import tweepy
from tweepy import OAuthHandler
import re

config = utils.get_config('config.ini')
print config
host = config['db']['host']
user = config['db']['user']
password = config['db']['password']
db_name = config['db']['dbname']

db = mdb.connect(user=user, host=host, password=password, db=db_name,  charset='utf8')


consumer_key = config['twitter']['consumer_key']
consumer_secret = config['twitter']['consumer_secret'] 
access_token = config['twitter']['access_token']
access_secret = config['twitter']['access_secret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def cities_input():
    return render_template("input_final.html")

@app.route('/index')
def testing_extender():
    return render_template('extender.html')



@app.route('/output_mvp')
def cities_output():
    user = request.args.get('ID')
    user = re.match('@?(.*)', user).groups()[0]
    cur = db.cursor()
    cur.execute("SELECT TWEET FROM tweets_by_user WHERE HANDLE='%s';" % user)
    query_results = np.array(cur.fetchall())
    if len(query_results) == 0:
        try:    
            stuff = api.user_timeline(screen_name = user, count = 8000, include_rts = False)
        
            for status in stuff:
                tweet =status.text
                screen_name = user
                cur.execute("INSERT INTO tweets_by_user (HANDLE, TWEET) VALUES (%s,%s)",(screen_name, tweet))
            db.commit()
            cur.execute("SELECT TWEET FROM tweets_by_user WHERE HANDLE='%s';" % user)
            query_results = np.array(cur.fetchall())
        except:
            return render_template('not_exist.html', user = user)
    tweets = [t[0] for t in query_results]
    vectorizer = joblib.load('/home/jtsitr/twitter_project/vectorizer.pkl')
    clf = joblib.load('/home/jtsitr/twitter_project/clf.pkl')
    tweets = vectorizer.transform(tweets)
    prediction = clf.predict(tweets)
    if tweets.shape[0]<100:
        return render_template('not_enough_tweets.html', user=user)
    else:
        the_result = np.mean(prediction)
        try:
            return render_template("output_final.html", the_result = the_result, user = user)
        except Exception as e:
            return render_template('500.html', error = str(e))




