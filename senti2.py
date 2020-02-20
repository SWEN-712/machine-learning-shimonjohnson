key = "058b861f487b4c3bb9707909e10fcb14"
endpoint = "https://athh.cognitiveservices.azure.com/"

# -*- coding: utf-8 -*-

import os
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from random import randint
import json

consumer_key = "VB8PDpUiWYNAGm57hRXCgWcHN" #twitter app’s API Key
consumer_secret = "OTQL6AGkgNCsjJtbo13wpmAwmy2RD7402HBIunxTfstToFTDo9" #twitter app’s API secret Key
access_token = "847539459486736384-3xuge9myxwwSIBAAncHfKVxC9O27xNT" #twitter app’s Access token
access_token_secret = "ZVsNfoRlaDw05V7vIgry80KkiBrFalWktLNG3Bj44x9LB" #twitter app’s access token secret


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

extracted_tweets = auth_api.user_timeline(screen_name = 'TwitterA11y', count =5, include_rts = False, tweet_mode = 'extended')
print(len(extracted_tweets))
final_tweets = [each_tweet.full_text for each_tweet in extracted_tweets]

finalJson = []
counter = 1
for tweet in final_tweets:
    # Preparing the data to give to Azure
    documents = {"id": counter, "language": "en", "text": tweet}
    counter = counter+1
    finalJson.append(documents)

def authenticateClient():
    credentials = CognitiveServicesCredentials(key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)
    return text_analytics_client


def sentiment():
    client = authenticateClient()
    try:
        response = client.sentiment(documents=finalJson)
        for document in response.documents:
          print("Document Id: ", document.id, ", Sentiment Score: ","{:.2f}".format(document.score))

        response = client.key_phrases(documents=finalJson)
        for document in response.documents:
            print("Document Id: ", document.id)
            print("\tKey Phrases:")
            for phrase in document.key_phrases:
                print("\t\t", phrase)

    except Exception as err:
      print("Encountered exception. {}".format(err))

sentiment()
