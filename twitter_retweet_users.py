#!/usr/bin/python
# -*- coding: utf-8 -*-

# Find all users who a tweet is retweeted from
#  either through the Twitter retweet mechanism supported by many Twitter clients
#  or by the user manually adding RT or via notations to the tweet

import re
import couchdb
import json
from twitter_DB import load_from_DB

# function to retrieve users who were retweeted
# Parameter:  tweet id
# Results:  list of user screen names

def get_rt_users(tweet):
    # regular expression adapted from Stack Overflow:  
    #  http://stackoverflow.com/questions/655903/python-regular-expression-for-retweets
    # this regex finds the text RT or via followed by some text with user names
    rt_patterns = re.compile(r"(RT|via)((?:\b\W*@[A-Za-z0-9_]+)+)", re.IGNORECASE)
    # given the retweet user name text found by the rt pattern, find one user name
    #   by giving a sequence of valid username characters (@ signs and other punctuation not included
    name_pattern = re.compile(r"([A-Za-z0-9_]+)")
    
    rt_users = []
    # first get users who retweeted using the Twitter retweet mechanism
    if tweet.has_key('retweeted_status'):
        # the retweeted_status field has a user and it has a field for user name
        #    standardize the name to lower case
        user = tweet['retweeted_status']['user']['screen_name'].lower()
        # print 'Found retweeted_status', user
        rt_users.append(user)
        
    # next inspect the tweet text for legacy retweet patterns such as RT and via
    try:
        mentiontext = rt_patterns.findall(tweet['text'])[0][1]
        # find the individual user names within the text
        mentions = name_pattern.findall(mentiontext)
        for mention in mentions:
            rt_users.append(mention)
    except IndexError, e:
            pass
    # filter out any duplicates by converting the list to a set (and then back to list)
    return list(set([rtu.lower() for rtu in rt_users]))

# the main program gets tweets from the DB and gets their retweets
if __name__ == '__main__':
    
    # give the data base name of one already saved in CouchDB
    DBname = 'search-elecciones2015'

    # get the tweets from the DB
    search_results = load_from_DB(DBname)
    print 'number loaded', len(search_results)
    
    for tweet in search_results:
        rt_user_names = get_rt_users(tweet)
        if len(rt_user_names) > 0:
            try:
                line = tweet['text'].encode('utf-8')
                print 'Tweet:', line
                print 'Retweets of: ',rt_user_names
            except UnicodeDecodeError:
                print "skipping non-utf-8 string"
            except UnicodeEncodeError:
                print "skipping non-utf-8 string"    
