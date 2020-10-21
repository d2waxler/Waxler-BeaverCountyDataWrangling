#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing useful python elements to examine data.
import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict
import re
import csv
import codecs
import cerberus
import sqlite3
import os
OSM_FILE = "BeaverCounty.osm" # My OSM file of Beaver County, PA 
SAMPLE_FILE = "BeaverCountySample.osm" 


zip_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

zip_types = defaultdict(set)

expected_zip = {}

def audit_zip_codes(zip_types, zip_name, regex, expected_zip):
    m = regex.search(zip_name)
    if m:
        zip_type = m.group()
        if zip_type not in expected_zip:
             zip_types[zip_type].add(zip_name)

def is_zip_name(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit(filename, regex):
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "way" or elem.tag == "node":
            for tag in elem.iter("tag"):
                if is_zip_name(tag):
                    audit_zip_codes(zip_types, tag.attrib['v'], regex, expected_zip)
    pprint.pprint(dict(zip_types))



#Did a test run on full OSM file, and it didn't take long, so I ran for the whole file here:
audit(OSM_FILE, zip_type_re)


for zip_type, ways in zip_types.items(): 
        for name in ways:
            if "-" in name:
                name = name.split("-")[0].strip()
            if "PA " in name:
                name = name.split("PA ")[1].strip('PA ')
            elif len(str(name))>5:
                name=name[0:5]
            elif name.isdigit()==False:
                print('OK')
            print(name)


# #### Noticed zip codes from well outside the area I'd selected on the map, are listed here, and some zip codes that just barely touch the county are also listed.

# In[ ]:




