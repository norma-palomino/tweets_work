#Assignment 4: collecting entities from tweet. Entity chosen: hashtags

# Goals:
#--make a function that takes a tweet as a parameter and returns a list of hashtags in that tweet
#--in the main program, get collection of tweets from DB using load_from_DB
#--for each tweet, call the function to get a list of entities for that tweet
#--add entities to a frequency dictionary
#--print out the top 20 entities and their frequencies

# Prof. MacCracken's program twitter_entities.py used as a base for own coding

from twitter_DB import load_from_DB

#first function: getting hashtags from a single tweet
def get_entities(tweet):
    #check if 'entities' is there
    if 'entities' in tweet.keys():
        #make a list of hashtags
        hashtag_list = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
        return hashtag_list
    else:
        #if no entities key, return empty lists
        return []

#second function: creating a dictionary of hashtags from a single tweet
def add_hashtags_to_dic(hashtag_list, hashtag_count):    
    #looping to find the text of the hashtag
    for text in hashtag_list:
        #converting all in lowercase so "elecciones" and "Elecciones" are counted as the same hashtag
        text = text.lower()
        #if the text is not in the dictionary
        if text != None: 
            if text in hashtag_count.keys():
                #add one count to that hashtag number
                hashtag_count[text] = hashtag_count[text] + 1
            #if not, add the first count for that hashtag            
            else:
                hashtag_count[text] =  1
    #get the count    
    return hashtag_count
        

if __name__ == '__main__':
    #DB of tweets: search results of two hashtags: "elecciones2015" or "eleccionesargentinas"
    DBname = 'search-elecciones2015oreleccionesargentinas'
    # load all the tweets
    tweet_results = load_from_DB(DBname)
    #show number loaded
    print 'number loaded', len(tweet_results) 
    
    #open dictionary counter     
    hashtag_count = {}
    
    #go through the first 100 tweets and find the hashtags
    for tweet in tweet_results[:100]:
        etiquetas = get_entities(tweet)
        #add hashtags from all tweets to one sigle dictionary
        hashtag_count = add_hashtags_to_dic(etiquetas, hashtag_count)
    #sort hashtags in reverse order (higher to lower frequency), and show the first 20
    for hashtag in sorted(hashtag_count, key=hashtag_count.get, reverse=True)[:20]:        
        #encoding for Spanish characters        
        try:
            encodedhash = hashtag.encode('utf-8')
            print encodedhash, hashtag_count[hashtag]
        except UnicodeDecodeError:
            print "skipping non-utf-8 string"
        except UnicodeEncodeError:
            print "skipping non-utf-8 string"          
       