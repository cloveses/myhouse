#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 19:27:42 2019

@author: haoshengxi
"""

# import psycopg2
# try:
#     conn = psycopg2.connect(host='127.0.0.1',port=50087, database='test',user='postgres', password='sunny13304918909')
#     print("database suc")
# except:
#     print("no")
import xml.sax

class articleHandler( xml.sax.ContentHandler ):

    def __init__(self):
        self.CurrentData = ""
        self.author=""
        self.title = ""
        self.year = ""
        self.journal = ""

    def startElement(self,tag,attributes):
        self.CurrentData=tag
        if tag=="article" :
            print("***article***")
            key=attributes["key"]
            print("key:",key)
            print("---这是一条分割线---")

    def endElement(self,tag):
        if self.CurrentData=="author":
            print("author:",self.author)
        if self.CurrentData=="title":
            print("title:",self.title)
        elif self.CurrentData=="year":
            print("year:",self.year)
        elif self.CurrentData=="journal":
            print("journal:",self.journal)

        # print(self.CurrentData, self.author, self.title, self.year, self.journal)
            # cur = connect.cursor()
            # cur.execute("INSERT INTO Article (pubkey,title,journal,year) VALUES ('1','2','3','4')")
            # cur.execute("INSERT INTO Article (pubkey,title,journal,year) VALUES (%s,%s,%s,%s)",(va,vb,vc,vd))

    def characters(self,content):
        if self.CurrentData=="author":
            self.author=content
        elif self.CurrentData=="title":
            self.title=content
        elif self.CurrentData=="year":
            self.year=content
        elif self.CurrentData=="journal":
            self.journal=content 
           
if __name__=="__main__":
    print("connected")
    parser=xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces,0)
    Handler=articleHandler()
    parser.setContentHandler(Handler)
    parser.parse("dblp.xml")
    

