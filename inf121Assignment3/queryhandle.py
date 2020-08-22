import json
import math
from collections import OrderedDict

from nltk.stem import PorterStemmer
#import myhelper
DOC_COUNT = 55482

#offsets, finalind, MAPPINGLIST


alloffsets = open("trackoffsets", "r")
OFFSETDATA = json.load(alloffsets)
alloffsets.close()
alph = []
for k in OFFSETDATA.keys():
    alph.append(k)
INV_INDEX = open("finalindex", "r")
KEEPSCORE = open("scores", "w+")
MAPPING = open("mapping_url", "r")
check_map = json.load(MAPPING)
#docscores = dict()

def main():

    while True:
        userin = input("Enter your search: ")
        searchterms = userin.split()
        ps = PorterStemmer()
        stemmed = []
        for w in searchterms:
            stemmed.append(ps.stem(w))
        bound = len(stemmed)
        for i in range(0, bound):
            #print(stemmed[i])
            if stemmed[i]==searchterms[i]:
                stemmed[i] = "_NULL"
                #del stemmed[i]
        setstem = set(stemmed)
        print(len (setstem))
        check = 0;
        for s in stemmed:
            if s== "_NULL" and check == 0:
                setstem.remove("_NULL")
                check = 1
        stemmed = list(setstem)

        #print(searchterms)
        print("---->", stemmed)
        getquery(searchterms, stemmed)


def display(newkeepscore):
    global MAPPING, check_map
    print("CALL DISPLAY__")
    print("SEARCH RESULTS: ")
    #check_map = json.load(MAPPING)
    #print(newkeepscore)

    shown = 0;
    for k,v in newkeepscore.items():
        #print("ooo ", k)
        #print(len(check_map))
        print(check_map[str(k)])
        shown+=1
        if shown>=50:
            break
    return
    #MAPPING.close()




def getdocs(for_term, for_stemmed, docs):
    global KEEPSCORE
    #tw = 0
    docscores = dict()
    for d in docs:
        #dtw = 0
        totalweight = 0
        for k,v in for_term.items():
            #calculate tf-idf here...

            for val in v:
                if val[0]==d: #just the doc-id looking for...
                    #get frequency
                    tf = 1+ (math.log(val[1]))
                    df = len(v)
                    idf = math.log(DOC_COUNT/df, 10)
                    tf_idf = tf*idf
                    totalweight += tf_idf
                    break
        for k,v in for_stemmed.items():
            print("LOOKED IN STEMMED.")
            #calculate tf-idf here...

            for val in v:
                if val[0]==d: #just the doc-id looking for...
                    #get frequency
                    tf = 1+ (math.log(val[1]))
                    df = len(v)
                    idf = math.log(DOC_COUNT/df, 10)
                    tf_idf = tf*idf
                    totalweight += tf_idf
                    break

        docscores[d] = totalweight
    newkeepscore = OrderedDict(sorted(docscores.items(), key=lambda t: t[1], reverse= True))
    #print("LEnzgTH: ", len(newkeepscore))
    #json.dump(newkeepscore, KEEPSCORE)
    #ocscores = newkeepscore
    #KEEPSCORE.close()
    display(newkeepscore)



    #docs = docs containing all terms



def getquery(terms, stemmedterms):
    global OFFSETDATA, INV_INDEX, alph
    #alphabet = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t']


    #print("-->", alph)
    trackdocs = dict()
    set_of_docs = set()
    list_of_docs = []
    for t in terms:
        #print("{",t,"}")
        key = t[0]
        if len(t)>1:
            key = key + t[1]
        seek_posit = OFFSETDATA[key] # jump to this spot in INV_INDEX
        s = alph.index(key)
        s +=1
        if s < len(alph):
            stopkey = alph[s]
            stop_posit = OFFSETDATA[stopkey]
        else:
            stop_posit = -1

        #print("Val got--> ", seek_posit)
        #print("Val stop-->", stop_posit)

        # seek to seek_posit
        # jsonload the readline
        # check if key is the (t)
        # --if YES:
            # get val:
        INV_INDEX.seek(seek_posit)
        position = seek_posit
        found = 0
        while stop_posit == -1 or position <= stop_posit:
            try:
                pullterm = json.loads(INV_INDEX.readline())
            except json.decoder.JSONDecodeError:
                break
            for k, v in pullterm.items():
                if k != t:
                    #print("{{", k)
                    #print("{{", t)
                    position = INV_INDEX.tell()
                    continue
                putval = []
                for val in v:
                    jval = json.loads(val)
                    #print("JVAL>>", jval)
                    set_of_docs.add(jval["docid"])
                    list_of_docs.append(jval["docid"])
                    value = (jval["docid"], jval["frequency"]) #tuple(doc, freq)
                    putval.append(value)
                trackdocs[k] = putval
                found = 1



            #position = INV_INDEX.tell()
            if found==1:
                #print("*****", pullterm)
                #print("FOUND!")
                #print(trackdocs)
                break
    stemdocs = dict()
    for t in stemmedterms:
        print("{",t,"}")
        key = t[0]
        seek_posit = OFFSETDATA[key] # jump to this spot in INV_INDEX
        s = alph.index(key)
        s +=1
        if s < len(alph):
            stopkey = alph[s]
            stop_posit = OFFSETDATA[stopkey]
        else:
            stop_posit = -1

        #print("Val got--> ", seek_posit)
        #print("Val stop-->", stop_posit)

        # seek to seek_posit
        # jsonload the readline
        # check if key is the (t)
        # --if YES:
            # get val:
        INV_INDEX.seek(seek_posit)
        position = seek_posit
        found = 0
        while stop_posit == -1 or position <= stop_posit:
            try:
                pullterm = json.loads(INV_INDEX.readline())
            except json.decoder.JSONDecodeError:

                break
            for k, v in pullterm.items():
                if k != t:
                    #print("{{", k)
                    #print("{{", t)
                    position = INV_INDEX.tell()
                    continue
                putval = []
                for val in v:
                    jval = json.loads(val)
                    #print("JVAL>>", jval)
                    value = (jval["docid"], jval["frequency"]) #tuple(doc, freq)
                    putval.append(value)
                stemdocs[k] = putval
                found = 1



            #position = INV_INDEX.tell()
            if found==1:
                #print("*****", pullterm)
                #print("FOUND!")
                #print("RESULT STEMDOCS: ", stemdocs)
                #print(type(stemdocs))

                break
    #INV_INDEX.close()
    #print("RESULT STEMDOCS: ", stemdocs)
    checklen = len(terms)
    relevantdocs = set()
    for s in set_of_docs:
        if list_of_docs.count(s) == checklen:
            relevantdocs.add(s)
    getdocs(trackdocs, stemdocs, relevantdocs)




main()