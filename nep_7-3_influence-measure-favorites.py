#Assignment #7, part 3: Creating and Influence Measure with Twitter tools 
#Part 3: Number of Tweets Favorited by Followers
#Goals:
#--Extracting favorited counts for each tweet in a particular user's timeline
#--Sum up favorited counts 
#--Print the total number of favorited counts for that user

#import required modules/functions
from twitter_login import oauth_login
from twitter_DB import load_from_DB

#function to get and return values from the 'favorite_count' field for each document (tweet) in the database
def total_favorites(doc):
    #look up for the field 'favorite_cont' in each tweet
    if 'favorite_count' in doc.keys():
        #add the value to a new variable fav_count_doc
        fav_count_doc = doc['favorite_count']
        #return the value
        return fav_count_doc

#main functon poiting at the user timeline database and running the function
if __name__ == '__main__':
    twitter_api = oauth_login()
    DBname = 'danielscioli-timeline'
    tweet_results = load_from_DB(DBname)
    #show number of tweets loaded    
    print 'number of tweets loaded', len(tweet_results)
    
    #open a list of favorite counts    
    fav_count_total=[]
    #pass each document in the database as argument of the 'total_favorites' function
    for doc in tweet_results:        
        favorites_items = total_favorites(doc) #the output value is assigned to the variable favorites_items
        #add each retweet count to the retweet_count_total list
        fav_count_total.append(favorites_items)
    
    #sum up retweet count valuesl assing the total value to the influence_retweets variable   
    influence_favorites = sum(fav_count_total)  
    
    #print the variable's output
    print "Total favorite counts for all twitter messages by Daniel Scioli: ", influence_favorites