#!/usr/bin/python
# -*- coding: utf-8 -*-

# This program takes a database stored in CouchDB and makes visualizations of 
#      a network of users connected by mentions or retweets in their tweets.
# It gets the network from twitter_retweet_mentions_network.py
# It reduces the network to a core of nodes with degree higher than some number
#      computed from the number of nodes in order to reduce the size of the graph
# It then writes a .dot file for viewing the graph in GraphViz.
#

import sys
import os
import json
import webbrowser
import codecs
import twitter
import networkx as nx
import couchdb
from twitter_DB import load_from_DB
import twitter_retweet_mentions_network


# Writes out a DOT language file that can be converted into an 
# image by Graphviz
def write_dot_output(g, out_file):

    out_file += ".dot"

    if not os.path.isdir(OUT_DIR):
        os.mkdir(OUT_DIR)

    try:
        nx.drawing.write_dot(g, os.path.join(OUT_DIR, out_file))
        print >> sys.stderr, 'Data file written to: %s' % os.path.join(os.getcwd(), OUT_DIR, out_file)
    except (ImportError, UnicodeEncodeError):

        # This block serves two purposes:
        # 1) Help for Windows users who will almost certainly not get nx.drawing.write_dot to work 
        # 2) It handles a UnicodeEncodeError that surfaces in write_dot. Appears to be a
        # bug in the source for networkx. Below, codecs.open shows one way to handle it.
        # This except block is not a general purpose method for write_dot, but is representative of
        # the same output write_dot would provide for this graph
        # if installed and easy to implement

        dot = ['"%s" -> "%s" [tweet_id=%s]' % (n1, n2, g[n1][n2]['tweetID'])
               for (n1, n2) in g.edges()]
        f = codecs.open(os.path.join(os.getcwd(), OUT_DIR, out_file), 'w', encoding='utf-8')
        f.write('''strict digraph {
    %s
    }''' % (';\n'.join(dot), ))
        f.close()

        print >> sys.stderr, 'Data file written to: %s' % f.name

        return f.name

# returns a copy of the graph in which all nodes of degree n or less are removed
def trim_degrees(g, degree=1):
    g2 = g.copy()
    d = nx.degree(g2)
    for n in g2.nodes():
        if d[n]<=degree: g2.remove_node(n)
    return g2


# the main program gets the graph and write the two visualization files
if __name__ == '__main__':
    # Put your tweet database here
    DB = 'search-elecciones2015oreleccionesargentinas'
    
    # if degree is 2, then nodes with degree 2 or greater are kept
    DEG = 2
    
    # An HTML page that we'll inject Protovis consumable data into
    HTML_TEMPLATE = 'twitter_retweet_graph.html'
    
    # variables for output directory and file names
    OUT = DB
    OUT_DIR = 'out'
    
    # get the tweets from the DB
    tweet_results = load_from_DB(DB)
    print 'number loaded', len(tweet_results)
    
    # get the graph connecting tweet authors to the retweets and mentions in their tweets
    g = twitter_retweet_mentions_network.make_network (tweet_results)
    
    removedegree = DEG -1
    core = trim_degrees(g, degree=removedegree)
    
    # Print out some stats
    print >> sys.stderr, "Number nodes:", g.number_of_nodes()
    print >> sys.stderr, "Num edges:", g.number_of_edges()
    #print >> sys.stderr, "Num connected components:", len(nx.connected_components(g.to_undirected()))
    #print >> sys.stderr, "Node degrees:", sorted(nx.degree(g))
    
    print >> sys.stderr, "Number core nodes:", core.number_of_nodes()
    print >> sys.stderr, "Num core edges:", core.number_of_edges()
    #print >> sys.stderr, "Num core connected components:", len(nx.connected_components(core.to_undirected()))
    
    # Write Graphviz output
    write_dot_output(core, OUT)
    
