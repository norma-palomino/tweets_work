#!/usr/bin/python
# -*- coding: utf-8 -*-

import couchdb
import json
from twitter_login import oauth_login
from twitter_request import make_twitter_request

# Contains two functions for processing twitter users
#   get_user_profile contacts Twitter to get user profiles from ids or screen_names
#   add_users_to_DB either creates or adds to a user database

# the user database will contain one document per user
# for each user, the DB entry includes fields:
#   screen_name,
#   user_id,
#   user_profile,      which will be the twitter user dictionary
#                      and which contains the friends, followers, statuses counts
#   optional fields are:
#   retweet_edges
#   mention_edges
#   friend_edges
#   follower_edges

# this function is from Matt Russell, 2nd edition of Mining the Social Web
#   modified to return dictionaries based only on screen_names
# Parameters:  twitter api object, with authorization
#    (optional) keyword arguments for user screen_names or user_ids
# Returns a dictionary with keys of the user screen_names and values are the user profiles
def get_user_profile(twitter_api, screen_names=None, user_ids=None):
    # must have either screen_name or user_id
    assert (screen_names != None) != (user_ids != None), 'Must have screen_names or user_ids, but not both'
    # initialize an empty dictionary for the result
    items_to_info = {}
    # adds whichever list is defined to an items list
    items = screen_names or user_ids
    
    # process all the items
    while len(items) > 0:
        # process 100 items at a time per the API specification for /users/lookup
        # see https://dev.twitter.com/docs/api/1.1/get/users/lookup for details
        # make a string with first 100 items separated by commas for the twitter lookup
        items_str = ','.join([str(item) for item in items[:100]])
        # reset items to remove first 100
        items = items[100:]
        
        if screen_names:
            response = make_twitter_request(twitter_api.users.lookup, screen_name=items_str)
        else:  # user_ids
            response = make_twitter_request(twitter_api.users.lookup, user_id=items_str)
            
        # for each user in the response, get their profile out of the response
        for user_info in response:
            # if screen_names passed in, return dict with screen_name keys
            if screen_names:
                items_to_info[user_info['screen_name']] = user_info
            else:
                # if user_ids passed in, return dict with user_id keys
                items_to_info[user_info['id']] = user_info
                
    return items_to_info

# This function by Nancy McCracken to create or add users to a database in CouchDB
#   If there is an existing database and if the entries have 'user_id' keys for users,
#      it will make sure that duplicate user entries are not created
#   The function twitter_DB.load_from_DB can be used to retrieve user entries from a database
# Parameters:  DataBase name
#     user profile dictionary - example is result of get_user_profile function above

def add_users_to_DB (DBname, user_profile_dict):
    # connect to database server and create db if needed
    server = couchdb.Server('http://localhost:5984')
    # use this list for previous data
    doclist = []
    # if you can't create a db of that name, assume that it already exists
    try:
        db = server.create(DBname)
        print "created new DB named", DBname
    except couchdb.http.PreconditionFailed, e:
        db = server[DBname]
        print "connected to existing DB named", DBname
        # get the data from the existing database to see if there are duplicates
        doclist = [db[key] for key in db]
    except ValueError, e:
        print "Invalid DB name" 
        sys.exit(0)    

    # make a list of all the users to add to the database
    #   where each list item is the DB dictionary described above
    user_list = []
    
    # make the DB dictionary for each user
    for user in user_profile_dict:
        userTwitterDict = user_profile_dict[user]
        userInfoDict = {}
        userID = userTwitterDict['id']
        userInfoDict['user_id'] = userID
        userInfoDict['screen_name'] = userTwitterDict['screen_name']
        userInfoDict['user_profile'] = userTwitterDict
        # check if this user is already in the database
        isFound = False
        for doc in doclist:
            if ('user_id' in doc.keys()) and (doc['user_id'] == userID):
                # skip this user
                print "User already in DB:", userInfoDict['screen_name']
                isFound = True
        # after all docs scanned, user is not already in DB
        # add this user dictionary to the list
        if not isFound:
            user_list.append(userInfoDict)
        
        
    # add the data to the database
    db.update(user_list, all_or_nothing=True) 
    print 'Added', len(user_list), 'users to DB:', DBname
   

# test program to get user profiles for multiple users and put them in a database
if __name__ == '__main__':
    twitter_api = oauth_login()
    
    print get_user_profile(twitter_api, user_ids=[132373965])
    
    users = ['SergioMassa','mauriciomacri','CFKArgentina','elisacarrio']
    user_profile_dict = get_user_profile(twitter_api, screen_names=users)
    
    # after calling this function, check couchdb to look at this database
    DBname = 'users-massamacricristinaelisacarrio'
    add_users_to_DB(DBname, user_profile_dict)
    