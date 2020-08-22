import re
import os
import json
import jsonpickle
from myindexer import Posting
from bs4 import BeautifulSoup
import sys

DOC_COUNT = 0

INV_LIST = dict()
RESOURCES = 0
TOTAL_TOKS = 0




DOC_COUNT = 0
MAPPINGLIST = dict()

allfiles = []
prefix = "indexerfile"




#data structure needed for mapping url to INT
    #in fxn: mapURLtoInt


def main():
    # os.walk to file

    global DOC_COUNT
    for root, dirs, files in os.walk(
            "/Users/katreenaerickson/Downloads/DEV"):
        for f in files:
            p = root + "/" + f
            print(p)
            jf = open(p)
            jsondata = json.load(jf)
            jf.close()
            #print("LOADED...")
            txtdata = getjson(jsondata)
            #print("GOT IT....")
            postings = parsedoc(txtdata)
            #print("~~~~~~~~~~~~ got new postings ~~~~~~~~~~~")
            #jf.close()

            for k, v in postings.items():
                #print("> > > > > > . . > . > >  entered loop")
                global INV_LIST
                #global TOTAL_TOKS
                if k not in INV_LIST.keys():
                    #print("adding to list here.....")
                    INV_LIST[k] = []
                #doc_id, frequency, fields

                newpost = Posting(DOC_COUNT-1, v[0], v[1])
                jnewpost = jsonpickle.encode(newpost)
                INV_LIST[k].append(jnewpost)

                ##added code to handle space
                ###
                #if len(INV_LIST)>=10000:
                if sys.getsizeof(INV_LIST)>=600000:
                    spacehandling()


        #DOC_COUNT+=1
    #print(INV_LIST)
    #printinfo()
    global RESOURCES
    print("TOTAL DOCS: ", str(DOC_COUNT))

    unify()
    print("RESOURCES: ", str(RESOURCES))
    #checker = open("indexerfile1")
    #checking = json.load(checker)

    #print(checking["scheduling"])
    #print(checking["verification"])

    #i = 5
    #for key in checking:
    #    if i>=0:
    #        print(key, "-->", checking[key])
    #    else:
    #        break
    #    i-=1




    # open file
    # pass content to getjson
    # jf = open(json_path)
    # jsondata = json.load(jf)
    # getjson(jsondata)



def printinfo():
    global INV_LIST
    for k, v in INV_LIST.items():
        print(k, "----> ", v)





def parsedoc(text):
    # result = set()
    #print("CALLED PARSEDOC!!!\n")
    result = dict()
    posit = 0
    text = text.lower()
    addthis = re.findall('[a-z0-9]+', text)
    for a in addthis:
        if a not in result.keys():
            result[a] = [1, [posit]]
        else:
            result[a][0] += 1
            result[a][1].append(posit)
        posit += 1
    #print("FINISHED PARSEDOC...")
    #print(result)

    return result




def getjson(json_dat):
    # mjson = json.loads(json_in)
    passurl = json_dat["url"]
    passurl = passurl.split('#')[0]
    mapUrltoInt(passurl)
    html = json_dat["content"]
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    alltext = soup.get_text()
    #print(alltext)
    return alltext


def mapUrltoInt(urlstring):
    # return int
    #print(">  >   >   > Call MAPURLTOINT  <")
    global DOC_COUNT, MAPPINGLIST
    MAPPINGLIST[DOC_COUNT] = urlstring
    DOC_COUNT +=1

    #temp = DOC_COUNT
    #DOC_COUNT += 1
    #return temp


def spacehandling():
    print("Called spacehandling!!!!")
    global INV_LIST, RESOURCES
    #sorted_inv = sorted(INV_LIST.keys())
    RESOURCES+=1
    fname = "indexerfile" + str(RESOURCES)

    with open(fname, "w+") as outindfile:
        #for k,v in INV_LIST.items():
        for k in sorted(INV_LIST):
            tempd = dict()
            tempd[k] = [INV_LIST[k]]
            #tempd[k] = [v]
            json.dump(tempd, outindfile)
            outindfile.write("\n")



    #json.dump(a_dict, allfiles[1], sort_keys= True, separators=(',', ': '))
    #allfiles[1].write("--------\n-----------------~~~")
    #json.dump(b_dict, allfiles[1], sort_keys= True, separators=(',', ': '))
    #an = json.loads(allfiles[1]["be"])
    #print(an)




    """with open(fname, "w+") as outfile:
        json.dump(INV_LIST, outfile, sort_keys=True)
    INV_LIST = dict()
    print("********")
    """
    INV_LIST = dict()
    '''
    global DOC_COUNT
    if RESOURCES==1:
        print("*********checking the resources*******")
        outa = open("indexfile1")
        #outb = open("indexfile2")
        ja = json.load(outa)
        print(ja)
        print("FINISH CHECK!!")
        #jb = json.load(outb)
        #print(jb)
        outa.close()
        #outb.close()
        '''
'''
def unify():
    global INV_LIST
    global RESOURCES
    tempdict = dict()
    if len(INV_LIST)!= 0:
        RESOURCES+=1
        lastfname = "indexfile" + str(RESOURCES)
        with open(lastfname, "w+") as outfile:
            json.dump(INV_LIST, outfile, sort_keys=True)
    while RESOURCES>=1:
        iterfilea = open("indexfile" + str(RESOURCES), "r")
        filea = json.load(iterfilea)


'''


offsets = dict()
finalind = open("finalindex", "w+")

def getmin(termlist):
    #global offsets
    #global finalind


    smallest = min(termlist)
    #if smallest[0] not in offsets.keys():
     #   offsets[smallest[0]] =finalind.tell()
    return smallest

def dumpurlinfo():
    global MAPPINGLIST
    outmapping = open("mapping_url", "w+")
    json.dump(MAPPINGLIST, outmapping)
    outmapping.close()


def unify():
    global INV_LIST, RESOURCES, offsets
    global finalind
    buffer = dict()
    #outbuffer = []
    allfiles = []

    if len(INV_LIST)>0:
        print("RES BEFORE: ", str(RESOURCES))
        spacehandling()

    checkmin = []

    for i in range(1, RESOURCES+1):
        afile = open("indexerfile"+str(i), "r")
        allfiles.append(afile)
        aline = json.loads(afile.readline())
        # appending a checkmin
        for k,v in aline.items():
            checkmin.append(k)
            if k not in buffer.keys():
                buffer[k] = v[0] #for key, pair with LIST of DICT_POSTINGS!
                #print("BUFFER[" + k+ "]--> ", v[0])
            else:
                value = buffer.get(k)
                value.extend(v[0]) #extend the value with additional postings!

    minbuff = []
    while len(allfiles)>0:
        smallterm = getmin(checkmin) #get smallest term

        ######CHECK FREQUENCY OF SMALLTERM
        #get index of smallest term and READLINE after processing it...
        td = dict()
        #print("gotten--", buffer.get(smallterm))
        td[smallterm] = buffer.get(smallterm)
        ####minbuff
        if checkmin.count(smallterm)==1:
            minbuff.append(td)
            del buffer[smallterm]
        #print("newmin: ", minbuff)

        #get index--index into checkmin & files!
        #print()
        c_ind = checkmin.index(smallterm)
        #print("index:", c_ind)
        #print("Length: ", len(allfiles))
        #print("checkmin len:", len(checkmin))
        try:
            checkentry = json.loads(allfiles[c_ind].readline())
            for k,v in checkentry.items():
                checkmin[c_ind] = k
                if k not in buffer.keys():
                    buffer[k] = v[0]  # for key, pair with LIST of DICT_POSTINGS!
                    # print("BUFFER[" + k+ "]--> ", v[0])
                else:
                    #print("~~~Calling else for: ", k)
                    value = buffer.get(k)
                    value.extend(v[0])
                    buffer[k] = value


        except json.decoder.JSONDecodeError:
            print("handle except...")
            allfiles[c_ind].close()
            allfiles.pop(c_ind)
            checkmin.pop(c_ind)
            continue

        if len(minbuff)>=10000:
            print("CALL DUMPING:")
            for i in minbuff:
                for k in i.keys():
                    if len(k)==1:
                        if k[0] not in offsets.keys():
                            print("Add this: ", k[0])
                            offsets[k[0]] = finalind.tell()
                    else:
                        newk = k[0]+k[1]
                        if newk not in offsets.keys():
                            offsets[newk] = finalind.tell()
                #print("MINBUFF item: ", i)
                json.dump(i, finalind)
                finalind.write("\n")
            minbuff.clear()
    if len(minbuff)>0:
        for i in minbuff:
            for k in i.keys():

                if k[0] not in offsets.keys():
                    print("--------> adding more to offsets")1
                    offsets[k[0]] = finalind.tell()

            json.dump(i, finalind)
            finalind.write("\n")
        minbuff.clear

    alloffsets = open("trackoffsets", "w+")
    json.dump(offsets, alloffsets)
    alloffsets.close()
    dumpurlinfo()
    finalind.close()








   # terms =dict() #use this to update buffer dictionary
    #checkmin = []

'''

    print("CALL UNIFY\n")
    for file in allfiles:

        aline = json.loads(file.readline())
        #just get key value from jsonload line:
        for k,v in aline.items():

            print("****", k)
            #check if key is in terms...
            #NO NEED TO DO MIN?
            #-->
                # if YES: iterate thru v to get the dict of the posting and append to the value held in terms.
            print("{}{}{}", v[0])
            print("TYPE: ", type(v[0]))
            for av in v[0]:
                print(av)
                print(type(av))
                aj = json.loads(av)
                print(":::", type(aj))
                print("_____", aj)
                print("------->", aj["frequency"])
            #np = Posting()


        print(type(aline))
        print(">>>>", aline, "<<<<")
    return




'''


main()
