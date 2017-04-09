#Assignment #7, part 1: Creating and Influence Measure with Twitter tools
#Part 1: Harvesting user's timeline
#(Note: although the assigment mentioned also Facebook, due to the scope of my doctoral work 
#I decided to focus on Twitter only)
#Goals:
#--harvesting tweets from user's timeline
#--saving results in a CouchDB database

#import required modules/functions
import sys
import json
from twitter_login import oauth_login
from twitter_DB import load_from_DB
from twitter_request import make_twitter_request
from twitter_DB import save_to_DB

#function for harvesting user tweets by Matthew Russell
#in his book "Mininig the Social Web", 2nd Ed.
#no changes made
def harvest_user_timeline(twitter_api, screen_name=None, user_id=None, max_results=2900):
    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"
    
    kw = { #Keyword args for the twitter API call
         'count': 200,
         'trim_user' : 'true',
         'include_rts' : 'true',
         'since_id' : 1
         }
    if screen_name:
        kw['screen_name'] = screen_name
    else:
        kw['user_id'] = user_id
        
    max_pages = 16
    results = []
    
    tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
    
    if tweets is None: #401 (Not Authorized) - Need to bail out on loop entry
        tweets = []
        
    results += tweets
    
    print >> sys.stderr, 'Fetched %i tweets' %len(tweets)
    
    page_num = 1
    
    if max_results == kw['count']:
        page_num = max_pages #Prevent loop entry
        
    while page_num < max_pages and len(tweets) > 0 and len(results) < max_results:
        kw['max_id'] = min([ tweet['id'] for tweet in tweets]) - 1
        
        tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
        results += tweets
    
        print >> sys.stderr, 'Fetched %i tweets' % (len(tweets),)
    
        page_num += 1
        
    print >> sys.stderr, 'Done fetching tweets'
    
    return results[:max_results]

#'__main__' function created for this particular program
if __name__ == '__main__':
    twitter_api = oauth_login()
    print "Twitter OAuthorization: ", twitter_api
    tweets = harvest_user_timeline(twitter_api, screen_name='danielscioli', max_results=2900)
    
    DBname = 'danielscioli-timeline1'

   # save the results to this database
    save_to_DB(DBname, tweets)
    print 'Saved to DataBase: ', DBname