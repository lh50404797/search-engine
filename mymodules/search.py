#!/usr/bin/env python
#coding=utf8

import os
import sys
from pyes import *
from Website.models import Results

PAGE_SIZE=10

def dosearch(string,upage,total_hits):
#     print string
#     print upage
#     print total_hits
    conn = ES('127.0.0.1:9200', timeout=3.5)#Connect to ES
#     print "Conn", conn
#     
#     fq_title = FieldQuery(analyzer='ik')
#     fq_title.add('title',string)
# #     
#     fq_content = FieldQuery(analyzer='ik')
#     fq_content.add('content',string)
# # 
#     bq = BoolQuery(should=[fq_title,fq_content])
# 
#     #add highlight to the search key word
    h=HighLighter(['<b>'], ['</b>'], fragment_size=100)
#     
    page = int(upage.encode('utf-8'))
    if page < 1:
        page = 1
# 
    q = StringQuery(string, "content")
#     s = Search(q,start=(page-1)*PAGE_SIZE,size=PAGE_SIZE)
    s=Search(q,highlight=h,start=(page-1)*PAGE_SIZE,size=PAGE_SIZE)
#     print s
    s.add_highlight("content")
#     s.add_highlight('title')
    results = conn.search(s,indices='tsinghua_spider',doc_types='searchEngine-type')
    for (k, v) in results.items() :
        print "dict[%s]=" % k,v
#     results=conn.search(s,indices='tsinghua_spider',doc_types='searchEngine-type')
#     results = conn.search(q)
    #return the total hits by using a list object
#     total_hits.append(len(results))
    total_hits.append(len(results))
    
    #print total_hits[0]

    list=[]
    hits = results['hits']['hits']
    for r in hits:
#         if(r._meta.highlight.has_key("title")):
#             r['title']=r._meta.highlight[u"title"][0]
#         if(r._meta.highlight.has_key('content')):
#             r['content']=r._meta.highlight[u'content'][0]
# 
        res = Results()
        res.content = r['highlight']['content'][0]
        res.title = r["_source"]['title']
        res.url = r["_source"]['url']
        res.content.encode('utf-8')
#         res.content = r['content']
#         res.title = r['title']
#         res.url = r['url']
        list.append(res)
    return list
