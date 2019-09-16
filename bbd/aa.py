import psycopg2
import xml.sax

# conn = psycopg2.connect(host='192.168.7.233', database='test',user='postgres', password='123456')
# cur = conn.cursor()

class articleHandler(xml.sax.ContentHandler):
    def __init__(self):
        xml.sax.ContentHandler.__init__(self)
        self.CurrentData = ""
        self.content = ""
        self.datas = {}
        self.key = ""

    def startDocument(self):
        self.conn = psycopg2.connect(host='127.0.0.1',port=50087, database='test',user='postgres', password='sunny13304918909')
        # self.conn = psycopg2.connect(host='192.168.7.233', database='test',user='postgres', password='123456')
        self.cur = self.conn.cursor()

    def endDocument(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def startElement(self,tag,attributes):
        self.CurrentData=tag
        if 'title' in self.datas and 'year' in self.datas and 'journal' in self.datas:
            print("datas:",self.key ,self.datas)
            self.cur.execute("INSERT INTO Article (pubkey,title,journal,year) VALUES\
             (%s,%s,%s,%s)",(self.key,self.datas['title'],self.datas['journal'],self.datas['year']))
            self.datas.clear()
        if tag=="article" :
            print("***article***")
            self.key=attributes["key"]
            print("key:",self.key)

    def endElement(self,tag):
        if self.CurrentData in ("title", "year", "journal"):
            self.datas[self.CurrentData] = self.content

    def characters(self,content):
        self.content = content.strip()
            
if __name__=="__main__":
        parser=xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces,0)
        Handler=articleHandler()
        parser.setContentHandler(Handler)
        parser.parse("dblp.xml")
