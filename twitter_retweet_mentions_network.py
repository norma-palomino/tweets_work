#!/usr/bin/python
# -*- coding: utf-8 -*-

# Make a network from the users who retweet a tweet and from user mentions
#   Make a directed edge from each retweet user to the author who tweeted them
#   Also make a directed edge from each user to the @ mentions in their tweet
# There are two versions of the program:  one that just makes the network from the tweet db
#   and another one that makes an accompanying users db with the mention and retweet edges
# This program also includes two helper functions for dealing with networks:
#   sorted_dict and trim_degrees

import couchdb
import json
import networkx as nx    
from twitter_DB import load_from_DB
from twitter_retweet_users import get_rt_users
from twitter_entities import get_entities
from operator import itemgetter
    
# this function makes the retweet and mention network from a tweet DB
# Parameters:  the list of tweets from the tweet DB
# Results:  a directed graph network
def make_network (tweetList):
    # initialize a directed graph
    g = nx.DiGraph()
    
    # for every tweet, add edges
    for tweet in tweetList:
        # get the author of the tweet (screen_name)
        author = tweet['user']['screen_name']
        # get retweet user names from the tweet
        rt_user_names = get_rt_users(tweet)
        # if the list is not empty, add the retweet edges
        if rt_user_names: 
            # add an edge from retweeted user to the author that retweeted them
            for rt_user in rt_user_names:
                g.add_edge(rt_user, author, {"tweetID": tweet["id"]})
        # get the lists of entities from the tweet
        mentions, hashtags, urls = get_entities(tweet)
        # if the mentions list is not empty, add the mention edges
        if mentions:
            # add an edge from the tweet user to each mention
            for mention in mentions:
                g.add_edge(author, mention, {"tweetID": tweet['id']})
            
    # give the size of the resulting graph
    print "number nodes", g.number_of_nodes()
    print "number edges", g.number_of_edges()
    # return the graph
    return g


# function that also makes a user DB is not yet written

# ## network helper functions
# define a dictionary sort on values in reverse order
def sorted_dict(d):
    sortedValueList = sorted(d.items(), key = itemgetter(1), reverse=True)
    return sortedValueList

# function to make a core graph of users with degree greater than 1
def trim_degrees(g, degree=1):
    g2 = g.copy()
    d = nx.degree(g2)
    for n in g2.nodes():
        if d[n]<=degree:
            g2.remove_node(n)
    return g2
# ##

# the main program tests the first function
if __name__ == '__main__':
    
    # give the data base name of one already saved in CouchDB
    DBname = 'search-eleccionesargentinas'

    # get the tweets from the DB
    tweet_results = load_from_DB(DBname)
    print 'number loaded', len(tweet_results)
    
    # get the graph connecting tweet authors to the retweets and mentions in their tweets
    g = make_network (tweet_results)
    
    # compute centrality measures in the Python shell after the program executes
    
    
    