#!/usr/bin/python
# -*- coding: utf-8 -*-

from twitter_DB import load_from_DB

# this program contains a function to return lists of some twitter entities

# for each tweet, this function returns lists of the entities:  mentions, hashtags, URLs
# Parameter:  a tweet (as a Twitter json object)
# Result:  3 lists of the above entities
def get_entities(tweet):
    # make sure this is a tweet by checking that it has the 'entities' key
    if 'entities' in tweet.keys():
        # list of mentions comes from the 'screen_name' field of each user_mention
        mentions = [user_mention['screen_name'] for user_mention in tweet['entities']['user_mentions']]
        
        # list of hashtags comes from the 'text' field of each hashtag
        hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]    
    
        # list of urls can come either from the 'url' field  or 'expanded_url' field of each url
        urls = [urlitem['url'] for urlitem in tweet['entities']['urls']]    
        urls = urls + [urlitem['expanded_url'] for urlitem in tweet['entities']['urls']]
        
        # we ignore the symbols and optional media entity fields
        return mentions, hashtags, urls
    else:
        # if no entities key, return empty lists
        return [], [], []

# the main program tests this function by loading all tweets from a search database
#   and printing the entities from the first 20 tweets
if __name__ == '__main__':
    # this should be the name of a DB with tweets
    DBname = 'search-elecciones2015'
    # load all the tweets
    tweet_results = load_from_DB(DBname)
    print 'number loaded', len(tweet_results) 
    
    # go through the first 20 tweets and find the entities
    for tweet in tweet_results[:20]:
        mentions, hashtags, urls = get_entities(tweet)
        print 'Mentions:', mentions
        print '  Hashtags:', hashtags
        print '  URLs: ', urls