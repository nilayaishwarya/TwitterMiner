import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener


def process_or_store(tweet):
    with open('data.json', 'w') as outfile:
        x = json.dumps(tweet)
        outfile.writelines(x)


consumer_key = '**'
consumer_secret = '**'
access_token = '**'
access_secret = '**'

print("Hello")

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    process_or_store(status._json)


class MyListener(StreamListener):

    def on_data(self, data):
        try:
            with open('iphone.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True


while True:
    try:
        twitter_stream = Stream(auth, MyListener())
        twitter_stream.filter(track=['#iphone11'])

    except Exception as  e:
        print(e)
        pass
