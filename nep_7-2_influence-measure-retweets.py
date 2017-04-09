#Assignment #7, part 2: Creating and Influence Measure with Twitter tools 
#Part 2: Number of Retweets as Influence Measure
#Goals:
#--Extracting retweet counts for each tweet in a particular user's timeline
#--Sum up retweet counts 
#--Print the total number of retweets for that user

#import required modules/functions
from twitter_login import oauth_login
from twitter_DB import load_from_DB

#function to get and return values from the 'retweet_count' field for each document (tweet) in the database
def total_retweets(doc):
    #look up for the field 'retweet_cont' in each tweet
    if 'retweet_count' in doc.keys():
        #add the value to a new variable,'retw_count_doc'
        retw_count_doc = doc['retweet_count']
        #return the value
        return retw_count_doc

#main functon poiting at the user timeline database and running the function
if __name__ == '__main__':
    twitter_api = oauth_login()
    DBname = 'danielscioli-timeline'
    tweet_results = load_from_DB(DBname)
    #show number of tweets loaded    
    print 'number of tweets loaded', len(tweet_results)
    
    #open a list of retweet counts    
    retw_count_total=[]
    #pass each document in the database as argument of the total_retweets function
    for doc in tweet_results:        
        retweet_items = total_retweets(doc) #the output value is assigned to the variable retweet_items
        #add each retweet count to the 'retweet_count_total' list
        retw_count_total.append(retweet_items)
    
    #sum up retweet count valuesl assing the total value to the influence_retweets variable   
    influence_retweets = sum(retw_count_total)  
    
    #print the variable's output
    print "Total retweets of Daniel Scioli's messages: ", influence_retweets