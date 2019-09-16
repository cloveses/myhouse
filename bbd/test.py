import psycopg2
import xml.sax

class articleHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.title = ""
        self.year = ""
        self.journal = ""
        self.key = ""

    def startElement(self,tag,attributes):
        self.CurrentData=tag
        print('startElement:', tag, )
        if tag=="article" :
            print("***article***")
            self.key=attributes["key"]
            print("key:",self.key)

    def endElement(self,tag):
        print('endElement:', tag, self.title, self.journal, self.year)

        # if self.CurrentData=="title":
        #     print("title:",self.title)
        # elif self.CurrentData=="journal":
        #     print("journal:",self.journal)
        # elif self.CurrentData=="year":
        #     print("year:",self.year)

    def characters(self,content):
        cur_content = content.strip()
        if self.CurrentData=="title":
            self.title=cur_content
        elif self.CurrentData=="year":
            self.year=cur_content
        elif self.CurrentData=="journal":
            self.journal=cur_content
            
if __name__=="__main__":
        parser=xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces,0)
        Handler=articleHandler()
        parser.setContentHandler(Handler)
        parser.parse("dblp.xml")
