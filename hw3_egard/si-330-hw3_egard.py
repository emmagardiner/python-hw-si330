__author__ = 'emmagardiner'
# -*- coding: utf-8 -*-
#!/usr/bin/python -tt

from bs4 import BeautifulSoup
import urllib2
import re
import json
import pydot

# Step 1. (10 points)
#
# Fetch the IMDB top 100 movies (by number of votes) page using this URL:
#
# http://www.imdb.com/search/title?at=0&sort=num_votes&count=100 (Links to an external site.)
#
# and save it in a HTML file named step1.html. The saved HTML file should look similar to
# (but does not have to be character-for-character identical to) step1_desired_output.html.
# Note that a few movies have titles or actors with, e.g. accented characters. Make sure you use the utf8 encoding
# to write out the HTML to use Unicode and preserve any non-English characters.


url = 'http://www.imdb.com/search/title?at=0&sort=num_votes&count=100'
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib2.Request(url, headers=hdr)
html = urllib2.urlopen(req)
content = html.read()
f = open(u'step1.html', 'w')
f.writelines(content)
f.close()


# FROM STACKOVERFLOW: problem-shooting HTTPError: HTTP Error 403: Forbidden
# site= "http://en.wikipedia.org/wiki/StackOverflow"
# hdr = {'User-Agent': 'Mozilla/5.0'}
# req = urllib2.Request(site,headers=hdr)
# page = urllib2.urlopen(req)

# Step 2. (25 points)
#
# Parse the HTML page above with BeautifulSoup, extract movie information as described below, and save
# the result in a tab-delimited file named step2.txt.  Your step2.txt file should have 3 columns and 100 rows.
# The 3 columns should be:
#
# IMDB_ID
# Rank
# Title
#
# The IMDB_ID is the part that sits between last two slashes in the movie URL in the table.
# For example, if the URL is http://www.imdb.com/title/tt0111161/, the IMDB ID is tt0111161
# Your tab-delimited step2.txt file should look a lot like step2_desired_output.txt.  However, we have noticed
# a bug in BeautifulSoup 4 that sometimes seems to truncate this top-100 table after the first 50 rows.
# So it's OK if your output (and mine) only have the top 50 movies.
#
# Here’s a sample of the first four lines:
#
# tt0111161   1     The Shawshank Redemption (1994)
# tt0468569   2     The Dark Knight (2008)
# tt1375666   3     Inception (2010)
# tt0110912   4     Pulp Fiction (1994)


f2 = open('step1.html')
soup = BeautifulSoup(f2, "html.parser")
tags = soup('a')
ID = []
TITLE = []
for tag in tags:
    id = re.findall(r'<a href="/title/(tt[0-9]{7})', str(tag))
    if id != [] and id not in ID:
        ID.append(id)
    title = re.findall('<a href="/title/tt[0-9]{7}/" title="(.+)">', str(tag))
    if title != []:
        TITLE.append(title)
#print ID
#print TITLE

tags2 = soup('td')
RANK = []
for tag in tags2:
    rank = re.findall(r'<td class="number">([0-9]{1,})', str(tag))
    if rank != [] and rank not in RANK:
        RANK.append(rank)
#print RANK

Z = zip(ID, RANK, TITLE)
#print Z

f = open('step2.txt', 'w')
for x in Z:
    f.write(x[0][0])
    f.write("\t")
    f.write(x[1][0])
    f.write("\t")
    f.write(x[2][0])
    f.write("\n")
f.close()


# Step 3. (20 points)
#
# Use the Web service http://omdbapi.com/ to get movie metadata for each of the top 100 movies using the IMDB ID
# you collected in Step 2.  The API with sample requests is documented on the homepage.
#
# For example, this URL fetches JSON for the movie “The Social Network”, which has IMDB ID tt1285016:
# http://www.omdbapi.com/?i=tt1285016 (Links to an external site.)
#
# You should see something like this JSON response:
# {"Title":"The Social Network","Year":"2010","Rated":"PG-13","Released":"01 Oct 2010","Runtime":"120 min",
# "Genre":"Biography, Drama","Director":"David Fincher","Writer":"Aaron Sorkin (screenplay), Ben Mezrich (book)",
# "Actors":"Jesse Eisenberg, Rooney Mara, Bryan Barter, Dustin Fitzsimons",
# "Plot":"Harvard student Mark Zuckerberg creates the social networking site that would become known as Facebook,
# but is later sued by two brothers who claimed he stole their idea, and the cofounder who was later squeezed out
# of the business.","Language":"English, French","Country":"USA","Awards":"Won 3 Oscars. Another 102 wins & 86
# nominations.","Poster":"http://ia.media-imdb.com/images/M/MV5BMTM2ODk0NDAwMF5BMl5BanBnXkFtZTcwNTM1MDc2Mw@@._V1_SX300.jpg",
# "Metascore":"95","imdbRating":"7.8","imdbVotes":"326,376","imdbID":"tt1285016","Type":"movie","Response":"True"}
#
# IMPORTANT!  You MUST pause 5 seconds between EVERY HTTP request to omdbapi.com. If you don’t do this, and send requests
# omdbapi.com continuously in a loop with no delay, the server may reject your requests AND MAY EVEN SHUT DOWN.
# (Yes, this has happened before.)
#
# Make sure you call the time module function sleep(5) after each HTTP request call to urlopen to pause for 5 seconds.
#
# Save your results in a text file named step3.txt that contains a JSON string for each movie on each line.
# The file should look like step3_desired_output.txt.

###################### STEP 3 CODE ###########################

# import time
# file = open('step3.txt', 'w')
# for x in ID:
#     url = str("http://www.omdbapi.com/?i="+x[0])
#     f = urllib2.urlopen(url)
#     read = f.read()
#     file.write(read)
#     file.write("\n")
#     time.sleep(5)
# file.close()


# Step 4. (20 points)
#
# After you verify that your step 3 output is correct, you can comment out your URL fetching code for step 3 to avoid
# running that time-consuming step from now on. Now open the file you saved in step 3, load the JSON string on each
# line into a variable, extract just the movie title and actors list, and save the results in a tab-delimited file named
# step4.txt.  There should be two columns in your tab-delimited step4.txt file:
#
# Movie name
# A JSON string containing the first 4 actors in the actors list.
# The first ten entries in your file should look like this (with a tab character between the movie name and actor list)
#
# The Shawshank Redemption   ["Tim Robbins", "Morgan Freeman", "Bob Gunton", "William Sadler"]
# The Dark Knight   ["Christian Bale", "Heath Ledger", "Aaron Eckhart", "Michael Caine"]
# Inception     ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page", "Tom Hardy"]
# Fight Club    ["Edward Norton", "Brad Pitt", "Helena Bonham Carter", "Meat Loaf"]
# Pulp Fiction   ["Tim Roth", "Amanda Plummer", "Laura Lovelace", "John Travolta"]
# The Lord of the Rings: The Fellowship of the Ring    ["Alan Howard", "Noel Appleby", "Sean Astin", "Sala Baker"]
# Forrest Gump   ["Tom Hanks", "Rebecca Williams", "Sally Field", "Michael Conner Humphreys"]
# The Matrix     ["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss", "Hugo Weaving"]
# The Lord of the Rings: The Return of the King     ["Noel Appleby", "Ali Astin", "Sean Astin", "David Aston"]
# The Godfather    ["Marlon Brando", "Al Pacino", "James Caan", "Richard S. Castellano"]



f3 = open('step3.txt').read()
movies = []
actors = []
f4 = open('step4.txt', 'w')
l = []
with open('step3.txt') as file:
    for line in file:
        x = json.loads(line)
        t = x["Title"].encode("utf-8")
        movies.append(t)
        a = x["Actors"].encode("utf-8").split(",")
        actors.append(a[0:4])
        f4.write(t)
        f4.write("\t")
        f4.write(str(a))
        f4.write("\n")




# Step 5. (20 points)
#
# In this step you’ll generate the DOT file containing the actor graph, using the pydot module as described in class.
# After downloading and install GraphViz from http://www.graphviz.org/ (Links to an external site.), you should install
# the pydot package in your usual way, e.g. pip install pydot or sudo pip install pydot. Read and try out the examples
# at http://pythonhaven.wordpress.com/tag/pydot/ (Links to an external site.)
#
# Now load the file you saved in step 4 and generate a graph using the actor lists. Each actor will be a graph node,
# and if two actors are in the actors list (of the first five actors, that is) for the same movie, then there will be an
# edge between them in the graph. Save the resulting graph in a .dot file, which is a plain text file in the DOT language.
#  Note that we don’t want to save a PNG file: we want the DOT file instead. The pydot manual at
# http://code.google.com/p/pydot/downloads/list (Links to an external site.) explains how to do this.
#
# Save your .dot file to a file called actors_graph_output.dot.  It should look like the file actors_graph_desired_
# output.dot supplied in the homework ZIP file.
#
# HINT:  Suppose A, B, C, D, E is the actors list for a movie. You’ll need to add edges for
# every possible pairs of actors in this list, e.g. (A, B)  (A, C) etc. This is where the optional itertools module
# will come in useful, if you choose to use it.  The combinations method will generate every possible pair of elements,
# given a list.




graph = pydot.Dot(graph_type='graph', charset="utf8")

with open('step4.txt') as file:
    for line in file:
        line = line.decode('utf-8')
        line = line.split('\t')
        a = line[1].split(", ")
        #print a
        for x in range(0, len(a)):
            n1 = pydot.Node(json.dumps((a[x]), ensure_ascii=False).encode('utf-8'))
            for y in range(x+1, len(a)):
                n2 = pydot.Node(json.dumps((a[y]), ensure_ascii=False).encode('utf-8'))
                edge = pydot.Edge(n1, n2)
                graph.add_edge(edge)
pydot.Dot.write(graph, "actors_graph_output.dot")



# Step 6. (5 points)
#
# Open the saved actors_graph_output.dot file you created in step 5 using the gvedit application that comes with
# GraphViz. Using the Graph/Settings dialog, save the graph visualization in a PNG image file named actors_graph.png.
# You can compare the left-most main graph in your result with the corresponding left-most graphs in the partial result
# file actors_graph_desired_output_sample.png provided in the homework ZIP file. (Note: Your PNG image file will be
# wider and have a bunch more little graphlets to the right, compared to the sample.)