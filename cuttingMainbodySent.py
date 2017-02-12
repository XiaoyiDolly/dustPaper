from pymongo import MongoClient
# from nltk.tokenize import sent_tokenize
from optSentCut import sentCut
from BeautifulSoup import BeautifulSoup
import re

pureLetterNum = set('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ,.-:')

client = MongoClient('localhost', 27019)
mainBodyCollecSrc = client.nasa_publication['mainbody']
mainBodyCollecDest = client.paper_content['indexed_paper_mainbody_sentences']
mainBodyCollecDest.drop()

allBody = list(mainBodyCollecSrc.find())

def saveDB(paper_id, sents):
    record = {}
    record['sentences'] = sents
    record['paper_id'] = paper_id
    mainBodyCollecDest.insert(record, check_keys=False)
    # print record

for i in range(len(allBody)):
    text = allBody[i]['mainbody_clean']
	#text = allBody[i]['mainbody'].replace('>', '> ').replace('<', ' <')
    #cleanr = re.compile('\\[.*?\\]')
    #text = re.sub(cleanr, ' ', text)
    #text = BeautifulSoup(text).text
    sent_tokenize_list = sentCut(text)
    
    clean_sents = {}
    idx = 0
    for sent in sent_tokenize_list:
        # sent  = "".join(filter(lambda x: x in pureLetterNum, sent))
        # clean_sents.append(sent)
        # clean_sents[str(idx)] = sent.strip()
        clean_sents['s_idx'] = idx
        clean_sents['text'] = sent.strip()
        saveDB(allBody[i]['document_id'], clean_sents)
        idx += 1
    print allBody[i]['document_id']
    

# import codecs
# for i in range(125, 131):
#     document = list(mainBodyCollecSrc.find({'document_id':str(i)}))[0]
#     print "-"*20 + str(i) + "-"*20
#     out = codecs.open(str(i) + "_mainbody.txt", 'w', encoding='utf-8')
#     text = document['mainbody'].strip()
#     if document['state'] == 'negative':
#         truncated_text = text[300:len(text)-2000]
#         out.write(truncated_text)
#         # print truncated_text
#     else:
#         # text = sent_tokenize(document['mainbody'])
#         # print text
#         out.write(text)
#     out.close()
