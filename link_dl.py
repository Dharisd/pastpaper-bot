import requests
from os import exists
import urllib.parse
from pp_db import getAllObjects

#get array of links
all_objects = getAllObjects()

#print the number of urls found
#print("{} urls found".format(len(all_objects)))

#generate file name of file to be downloaded from filename array
def genName(filenameArray,subject):
    name = subject +" "
    name += " ".join(str(x) for x in filenameArray)
    return name


#download the files
for x in all_objects:
    subject = x["subject"]
    file_url = x["url"]
    filenameArray = x["filename"]
    filename  = genName(filenameArray,subject)

    #print the current file name
    print(filename)
    file_dir = "files/" + filename 

    #only download if not found
    if exists(file_dir):
    
        #get file with requests
        req = requests.get(file_url)

        with open(file_dir, 'wb') as f:
            f.write(req.content)
