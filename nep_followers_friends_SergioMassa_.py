#Assignment 5: intersecting friends and followers of a single Twitter user

# Goals:
#--write a program that computes the ids of users who are both friends and followers of a twitterer
#--first, collect data for that user
#--use set(list) to convert followers and friends lists into sets, then look for intersections of ids

#import required modules/functions
from twitter_login import oauth_login
from twitter_DB import load_from_DB
from sets import Set

#new function to create the lists of followers and friends:
def friends_and_followers(doc):
    #get ids from the 'friend_edges' field in the database
    if 'friend_edges' in doc.keys(): 
        #open de list
        flist = []        
        #append each element (id) from the 'friend_edges' field
        for x in doc['friend_edges']:
            flist.append(x)
        #print the output, just to check results and how the program is going
        print "Number of friends: ", len(flist) 

    #same process for followers, extracting ids from the 'follower_edges' field:
    if 'follower_edges' in doc.keys():
        followlist = []        
        for x in doc['follower_edges']:
            followlist.append(x)
        print "Number of followers: ", len(followlist) 

    #convert the output lists into sets
    flist = Set(flist)
    followlist = Set(followlist)
    #intersect the sets
    both_friends_followers = flist.intersection(followlist)
    return both_friends_followers
            

if __name__ == '__main__':
    twitter_api = oauth_login()
    DBname = 'users-sergiomassa-+-only'
    ff_results = load_from_DB(DBname)
    print 'number loaded', len(ff_results)
    
    #pass the database item as argument of the created function
    for doc in ff_results:
        together = friends_and_followers(doc)
        #print the output
        print "Friends and Followers of Sergio Massa: ", together  
    
    #NOTE: the output of this intersection is an empty set. I double checked by processing the same lists of
    #friends (765) and followers (2000) in Excel, looking for duplicates, and found none.