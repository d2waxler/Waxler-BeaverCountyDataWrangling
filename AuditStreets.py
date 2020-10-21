#!/usr/bin/env python
# coding: utf-8

# In[8]:


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
SAMPLE_FILE = "BeaverCountySample.osm" # My sample file to be created below 
# Auditing Street Names
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons","Freeway","Circle","Strand","Sterling","Way","Highway",
            "Terrace","South","East","West","North"]

# Here are the corrections for different road/street types, Referenced from Udacity Course & GitHub; 
# I also added a few I noticed in my listings.
mapping = {
            " St ": " Street ",
            " St.": " Street ",
            " Rd.": " Road ",
            " Rd": " Road ",
            " rd": " Road ",
            " Ave ": " Avenue ", 
            " Ave.": " Avenue ",
            " Av ": " Avenue ", 
            " Dr ": " Drive ",
            " Dr.": " Drive",
            " Blvd": " Boulevard ",
            " Blvd": " Boulevard",
            " Blvd.": " Boulevard",
            " Ct": " Centre ",
            " Ctr": " Centre",
            " Pl ": " Place ",
            " Ln": " Lane ",
            " Cir ": " Circle ",
            " Wy": " Way ",
            " Tpke": " Turnpike ",
            " S ": " South ",
            " E ": " East ",
            " W ": " West ",
            " N ": "North"
}


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(filename):
    f = open(filename, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
            elem.clear()        
    f.close()
    return street_types

def update_name(name, mapping):
    for key,value in mapping.items():
        if key in name:
            return name.replace(key,value)
    return name        

st_types = audit(OSM_FILE)

pprint.pprint(dict(st_types))
for st_type, ways in st_types.items():
    for name in ways:
        better_name = update_name(name, mapping)
        print (name, "=>", better_name)


# In[ ]:




