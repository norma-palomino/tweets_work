#!/usr/bin/python
# -*- coding: utf-8 -*-

# This program is an example of the type of program that can make a collection
#    of tweets around a particular topic
import sys
import couchdb
import json
from twitter_login import oauth_login
from twitter_search import twitterSearch
from twitter_search import getEarliestID
from twitter_DB import save_to_DB

# the main program gets a twitter search, saves the results in a DB
#    and returns the max_id tweet number
# rerunning the program will add tweets before that one
# this is not guaranteed to have no duplicates, so should also remove
#    duplicates before using the collection, e.g. for frequencies
if __name__ == '__main__':
    twitter_api = oauth_login()
    print "Twitter OAuthorization: ", twitter_api
    # define the topic query
    # if you put additional keywords with a "space", Twitter interprets it as "and"
    # if you want either keyword (or both), use the OR operator
    query = '#eleccionesargentinas OR #elecciones2015'
    
    # edit this statement to add the early id from a previous search
    MAX_ID = ''
    
    KW = { }
    if not MAX_ID == '':
        KW['max_id'] = MAX_ID
    
    # access Twitter search - change the max_results to 1000 for the most tweets at one time
    result_tweets = twitterSearch(twitter_api, query, max_results=1000, **KW)
    print 'Number of result tweets: ', len(result_tweets)
    
    # choose a database name for your collection
    #   couchDB names have to be in lowercase letters
    #   and also cannot contain special characters like hashtags and spaces
    DBname = 'search-elecciones2015oreleccionesargentinas'
    
    # save the results to this database
    save_to_DB(DBname, result_tweets)
    print 'Saved to DataBase: ', DBname
    
    # get one of the earliest ids for the next iteration
    earlyID = getEarliestID(result_tweets)
    print 'Use this id for max_id (in quotes) in next search on the same topic', earlyID   
