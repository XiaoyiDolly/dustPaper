from pymongo import MongoClient
import pprint
from lxml import etree
from bs4 import BeautifulSoup
import re

client = MongoClient('localhost', 27019)
db = client.nasa_publication


def update_reference():
    collection = db.references
    for ref in collection.find():
        reference_list = ref["reference"] # a field
        new_ref = list()
        for x in reference_list:
            tree = etree.fromstring(x)
            for child in tree:
                if(child.tag=='cite'):
                    str = "<li>"+etree.tostring(child, encoding='unicode', method='html')+"</li>"
                    # print(etree.tostring(child, encoding='unicode', method='html'))
                    print(str)
                    new_ref.append(str)
                    continue
        collection.update_one({
            'document_id': ref["document_id"]
        }, {
            '$set': {
                'reference': new_ref
            }
        })

def update_plaintext():
    collection = db.plain_text
    with open("a.html","w") as file1,open("b.html","w") as file2:
        for doc in collection.find():
            text = doc["plain_text"].encode('utf-8').decode('ascii', 'ignore')
            soup = BeautifulSoup(text)
            # file1.write(soup.prettify())
            [x.extract() for x in soup.findAll('span')]
            [x.extract() for x in soup.findAll('a')]
            [x.extract() for x in soup.findAll('button')]
            str = ' '.join(soup.findAll(text=True))
            str = re.sub(r' \[( *;)* *\]',"",str)
            str = re.sub(r' +', " ", str)
            print(str)

            collection.update_one({
                'document_id': doc["document_id"]
            }, {
                '$set': {
                    # 'plain_text': html_str,
                    'plain_text_clean': str
                }
            })

def update_mainbody():
    collection = db.mainbody
    for doc in collection.find():
        text = doc["mainbody"]
        soup = BeautifulSoup(text)
        # print(soup.get_text())
        [x.extract() for x in soup.findAll('span')]
        [x.extract() for x in soup.findAll('a')]
        [x.extract() for x in soup.findAll('button')]
        str = ' '.join(soup.findAll(text=True))
        str = re.sub(r' \[( *;)* *\]', "", str)
        str = re.sub(r' +', " ", str)
        print(str)

        collection.update_one({
            'document_id': doc["document_id"]
        }, {
            '$set': {
                # 'mainbody':html_str,
                'mainbody_clean': str
            }
        })

def update_sections():
    collection = db.sections
    cleancollection = db.sections_clean
    for doc in collection.find():
        for key in doc.keys():
            if key!="document_id" and key!="_id":
                text = doc[key]
                soup = BeautifulSoup(text)
                [x.extract() for x in soup.findAll('span')]
                [x.extract() for x in soup.findAll('a')]
                [x.extract() for x in soup.findAll('button')]
                str = ' '.join(soup.findAll(text=True))
                str = re.sub(r' \[( *;)* *\]', "", str)
                str = re.sub(r' +', " ", str)
                print(str)
                cleancollection.update_one({
                    'document_id': doc["document_id"]
                }, {
                    '$set': {
                        key: str
                    }
                })

update_plaintext()
# update_mainbody()
update_sections()