Katreena Erickson
netID: kiericks

The zip contains (3) essential files:
1) The indexer.py contains code to build the partial and final indexes
2) The queryhandle.py contains code to receive search terms from user and return the search results
3) The myindexer.py holds the Posting class that is used in building the indexes



Queries:
1) artificial intelligence
2) professor gassko
3) wics community newsletter
4) computer machine learning
5) machine learning
6) compsci 171
7) uci news
8) uci ai club
9) inf 141
10)eppstein publications
11)uci social sciences
12)raymond klefstad
13)uci research
14)information retrieval research
15)uci admissions
16)faculty el zarki
17)uci hackathon
18)uci esports
19)informatics department
20)machine learning faculty



Testing & Improving:

- Queries regarding faculty were the quickest to process and return fairly accurate answers
- Queries holding 3 or more search terms generally took longer. I attempted to fix this by 
not using the porter stemmer for these longer queries as I counted on the number of search terms to make up for loss of accuracy
- Certain queries that were general, like artificial intelligence and 'uci news' took longer, most likely due to the large amount of relevant documents found overall, and the ordering it took. I tried to cut this back by improving my method of tracking offsets within the large index file. Instead of just providing offsets by the first letter, I did it by the first two letters.