#Assignment #7, part 4: Creating and Influence Measure with Twitter tools 
#Part 4: Count of Tweets that have been Retweeted and Favorited
#Goals: for a particular user's timeline:
#--Identify tweets that have been both retweeted and favorited 
#--Count those tweets and print the value 


#import required modules/functions
from twitter_login import oauth_login
from twitter_DB import load_from_DB

#function to get and return values from the 'favorite_count' field for each document (tweet) in the database
def fav_retweeted(doc):
    #check if both 'favorite_count' and 'retweet_count' field have values in each tweet
    for keys in doc:    
        if doc['favorite_count'] >0 and doc['retweet_count'] >0:
            #print doc['favorite_count'], doc['retweet_count'] #used for verification only
            #print doc['id_str'] #also for verification
                #(note: Twitter documentation recommends using id_str instead of id)
            #return id to be used by __main__
            return doc['id_str']
     

#main functon poiting at the user timeline database and running the function
if __name__ == '__main__':
    twitter_api = oauth_login()
    DBname = 'danielscioli-timeline1'
    tweet_results = load_from_DB(DBname)
    #show number of tweets loaded    
    print 'number of tweets loaded', len(tweet_results)
    
    #open a list     
    fav_retw_tweets=[]
    #pass each document in the database as argument of the fav_retweeted function
    for doc in tweet_results:        
        fav_retw_items = fav_retweeted(doc) #the output value is assigned to the variable fav_retw_items
        if fav_retw_items !=None:
        #add each fav_retweeted count to the fav_retw_items list
            fav_retw_tweets.append(fav_retw_items)
        #print fav_retw_tweets #for verification only
    
    #return the length of the list, i.e. count of tweets' ids that have been retweeted and favorited   
    influence_fav_retw = len(fav_retw_tweets)  
    
    #print the variable's output
    print "Daniel Scioli's tweets that have been favorited and retweeted: ", influence_fav_retw