#-*- coding:utf-8 -*-
import pymongo
import json
#链接mongo用户
client = pymongo.MongoClient('mongodb://localhost:27017')

db_keywords = client['tweetkeywords']
collection_keywords = db_keywords.tweets
# print(collection_keywords)

user_id_kw=[]
tweet_location_kw=[]
retweeted_kw =[]
quotation_kw = []


#d1=collection_keywords.count_documents({'retweeted_status':{'$ne':None}})
#print(d1)
ids_with_no_retweeted_status = []
for item in collection_keywords.find({}):
    if 'retweeted_status' not in item:
        ids_with_no_retweeted_status.append(item['id'])

print(ids_with_no_retweeted_status)



# for item in collection_keywords.find({}):
#     print(item)
#     user= eval(str(item['user']))
#     user_id_kw.append(user['id'])
#     tweet_location_kw.append(item['geo'])
#     quotation_kw.append(item['is_quote_status'])
#     if 'retweeted_status' in item:
#         retweeted_kw.append(item['retweeted_status'])

        
# def retweetedcount_kw():
#     print("\n The statistics about retweet: ")
#     retweetscount_kw = {}
#     for item in set(retweeted_kw):
#         retweetscount_kw.update({item: retweeted_kw.count(item)})
#     print(retweetscount_kw)
#     for idcode, number in retweetscount_kw.items():
#         re_tweets_kw = 0
#         if number is True:
#             re_tweets_kw = re_tweets_kw + 1
#         else:
#             pass
#     print("\n The number of repeated tweets: " + str(re_tweets_kw))
