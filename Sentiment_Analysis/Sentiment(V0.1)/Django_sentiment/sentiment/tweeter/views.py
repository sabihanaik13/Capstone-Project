from django.shortcuts import render
from django import forms


import requests
import glob
from bs4 import BeautifulSoup
import pandas as pd
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class NameForm(forms.Form):
    company = forms.CharField(label='company', max_length=100)


def fetch(request):
    labels = ['neutral_tweet' , 'Negative_tweet' , 'Positive_tweet' ]
    values = [33 , 33 , 34]

    if request.method == 'POST':
        company = ''
        form = NameForm(request.POST)

        company = request.POST.get('company')




        class TwitterClient(object):

            def __init__(self):

                # keys and tokens from the Twitter Dev Console
                consumer_key = 'D6MkertW4Sj8rBSYoOsbvdhJl'
                consumer_secret = 'EldSKoYJlcXgHb2mbYqv7FZd98nOhmdex8sSmiTdarEjK5iGUM'
                access_token = '983592056445534210-vbGACTti0KK8fxa7fVks7qnlnHDFgxM'
                access_token_secret = '2IA4ordLzeGu48T9MgdzCQ62n2hiINrjnyzAMK9y84gau'

                # attempt authentication
                try:
                    # create OAuthHandler object
                    self.auth = OAuthHandler(consumer_key, consumer_secret)
                    # set access token and secret
                    self.auth.set_access_token(access_token, access_token_secret)
                    # create tweepy API object to fetch tweets
                    self.api = tweepy.API(self.auth)
                except:
                    print("Error: Authentication Failed")

            def clean_tweet(self, tweet):

                return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)" , " ", tweet).split())

            def get_tweet_sentiment(self, tweet):

                # create TextBlob object of passed tweet text
                analysis = TextBlob(self.clean_tweet(tweet))
                # set sentiment
                if analysis.sentiment.polarity > 0:
                    return 'positive'
                elif analysis.sentiment.polarity == 0:
                    return 'neutral'
                else:
                    return 'negative'

            def get_tweets(self, query, count = 10):

                tweets = []

                try:
                    fetched_tweets = self.api.search(q = query, count = count)
                    for tweet in fetched_tweets:
                        parsed_tweet = {}
                        parsed_tweet['text'] = tweet.text
                        parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                        if tweet.retweet_count > 0:
                            if parsed_tweet not in tweets:
                                tweets.append(parsed_tweet)
                        else:
                            tweets.append(parsed_tweet)

                    return tweets

                except tweepy.TweepError as e:
                    print("Error : " + str(e))

        api = TwitterClient()
        tweets = api.get_tweets(query = company, count = 200)

        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        values = [(100*(len(tweets) -len( ntweets) - len(ptweets))/len(tweets)) , (100*len(ntweets)/len(tweets))  , (100*len(ptweets)/len(tweets))]
        return render(request, 'myapp/company.html', { 'company': company , 'values' : values })

    else:
        company = 'cipla'
        return render(request, 'myapp/company.html', { 'company': company ,  'values' : values })


def chart(request):
    return render(request, 'myapp/chart.html')


def company(request):
	if request.method == 'POST':
		form = NameForm(request.POST)
		print(form)
		return render(request, 'myapp/company.html', {'company': company ,  'values' : values})
