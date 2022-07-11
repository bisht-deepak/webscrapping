#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing required libraries
from bs4 import BeautifulSoup
import re
import requests
import pandas


# In[2]:


#for extracting contact info
def extracting_icon_set(html_code):
    style_tag= html_code.find_all("style", {"type": "text/css"})
    required_style_tag_string= str(style_tag[1])
    icons_list= re.findall("(icon-\w{1,3}):before", required_style_tag_string)
    return icons_list

def creating_icon_dict(BeautifulSoup):
    listof_values= [0,1,2,3,4,5,6,7,8,9,"+"," ",")","("]
    icons_dict= dict(zip(extracting_icon_set(html_code), listof_values))
    return icons_dict


# In[ ]:


#url to fetch
baseURL=input("Enter repository link:")
numofPages= input("Enter the number of pages: ")


# In[ ]:


#example of repository link
#"https://www.justdial.com/Bangalore/Corporate-Gift-Manufacturers/nct-10138715"

#to find the number of pages
#scroll to the bottom of the justdial page and look for the page index at right corner


# In[3]:


headers= {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
    }
#creating a new list to store the extracted info
List= []

for pageNum  in range(1,numofPages+1):                                         #improvization possible    
    req = requests.get(baseURL+"page-"+str(pageNum), headers= headers)

    #Get the data from the requested source
    data=req.text
    #using Beautiful Soup to get data from the website
    soup=BeautifulSoup(data, "html.parser")
    #creating dict for phone number extraction
    icons_dict= creating_icon_dict(soup)
    #accessing indiuvdual data cells
    stem= soup.find_all("li", {"class":"cntanr"})
    
    

    for i in range(10):                                            #improvization possible
        d={}

        #extracting name
        branchName= stem[i].findChildren("span", {"class":"lng_cont_name"})
        d["Name"]= branchName[0].text

        #extracting rating
        branchRating= stem[i].findChildren("span", {"class":"green-box"})
        d["Rating"]=branchRating[0].text

        #extracting address
        branchAddress= stem[i].findChildren("span", {"class":"cont_fl_addr"})
        d["Address"]=branchAddress[0].text
        branchOfferings= stem[i].findChildren("a", {"class": "lng_commn"})

        #extracting offerings
        for j in range(len(branchOfferings)):
            d["Offerings"]= branchOfferings[j].text.replace("\n","").replace("\t", "")

        #extracting contact info
        branchContact= stem[i].findChildren("span", {"class": re.compile("mobilesv icon-")})
        icon_str= str(branchContact)
        icons= re.findall("icon-\w{1,3}", icon_str)
        contact_str= ""
        for icon in icons:
            contact_str+= str(icons_dict[icon])
        d["Contact Info"]= contact_str 

        List.append(d)


# In[5]:


dF= pandas.DataFrame(List)


# In[6]:


dF


# In[7]:


dF.to_csv("JD.csv")

