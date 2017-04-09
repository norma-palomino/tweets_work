
from twitter_DB import load_from_DB

# this program contains a function to return lists of some twitter entities
# for each tweet, this function returns lists of the entities:  mentions, hashtags, URLs
# Parameter:  a tweet (as a Twitter json object)
# Result:  3 lists of the above entities
def get_entities(tweet):
    # make sure this is a tweet by checking that it has the 'entities' key
    if 'entities' in tweet.keys():
        # list of hashtags comes from the 'text' field of each hashtag
        hashtag_list = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]   
        # we ignore the symbols and optional media entity fields
        return hashtag_list
    else:
        # if no entities key, return empty lists
        return []
    
def hashtags_dic(hashtag_list):    
    #open dictionary counter     
    hashtag_count = {}
    #looping to find the text of the hashtag
    for text in hashtag_list:    
        if text != None: 
            if text in hashtag_count.keys():
                hashtag_count[text] = hashtag_count[text] + 1
            else:
                hashtag_count[text] =  1
    return hashtag_count
        
        

# the main program tests this function by loading all tweets from a search database
#   and printing the entities from the first 100 tweets
if __name__ == '__main__':
    # this should be the name of a DB with tweets
    DBname = 'search-eleccionesargentinas'
    # load all the tweets
    tweet_results = load_from_DB(DBname)
    print 'number loaded', len(tweet_results) 
    
    # go through the first 100 tweets and find the entities
    for tweet in tweet_results[:100]:
        etiquetas = get_entities(tweet)
        dic=hashtags_dic(etiquetas)
        print '  Hashtags:', etiquetas[:20]
        print ' Hastags count: ', dic
  
