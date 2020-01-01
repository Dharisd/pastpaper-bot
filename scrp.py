from bs4 import BeautifulSoup
import requests
import re
import argparse
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["pastpaperdb"]
mycol = mydb["pastpaperdata"]

#scraping physics and maths tutor to make past papers more accessible
ap = argparse.ArgumentParser()

ap.add_argument("-u", "--url", required=True,
   help="the url of the page")

args = vars(ap.parse_args())

#this should be cli argumant 
phy_url = args["url"] 

#gets all links from the page
def get_links(url):
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.text,features="html.parser")
    a_tags = soup.find_all('a', href=re.compile(r'(.pdf)'))


    #get all links
    links = []
    for tag in a_tags:
        link = tag["href"]
        gen_link = "https://www.physicsandmathstutor.com/" + link[62:]
        links.append(gen_link)
    return links


links = get_links(phy_url)


#for l in links:
#    print(l +"\n")



#function to parse links should return dictionary
def parse_link(link):
    #dict to to house all the wanted data
    parsed_data = {}
    split_url = link.split("/") # this is already valubale
    #print(split_url)
    filename = split_url[-1].split(" ") # a list of features

    
    parsed_data["subject"] = split_url[4].lower()
    #maths is a special case so handle it
    if parsed_data["subject"] == "maths":
        parsed_data["unit"] = filename[-2]
    else:
        parsed_data["unit"] = split_url[8][-1]
    
    #try to get the session(june/October)
    months = ["january","october","february","june"]
    if filename[0].lower() in months:
        parsed_data["session"] = filename[0].lower()
    
    #get the year of the session
    if filename[1].isdigit() and len(filename[1]) == 4:
        parsed_data["year"] = filename[1] 
    
    #get type of the paper
    if "MS" in filename:
        parsed_data["type"] = "ms"
    #there must be a better wayy
    elif "QP" in filename:
        parsed_data["type"] = "qp"

    #check for ial
    if "(IAL)" in filename:
        parsed_data["ial"] = "true"
    else:
        parsed_data["ial"] = "false"

    if "(R)" in filename:
        parsed_data["repeat"] = "true"
    else:
        parsed_data["repeat"] = "false"
    
    parsed_data["url"] = link

        

    
    parsed_data["filename"] = filename



    return parsed_data

# this parses all found links
for l in links:
    parsed = parse_link(l)
    x = mycol.insert_one(parsed)
    print(parsed)


