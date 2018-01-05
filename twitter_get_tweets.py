import twitter
import yaml

with open("twitter_keys.yml", "r") as f:
    keys = yaml.load(f)

CONSUMER_KEY = keys['Consumer Key']
CONSUMER_SECRET_KEY = keys['Consumer Secret']
ACCESS_TOKEN = keys['Access Token']
ACCESS_TOKEN_SECRET = keys['Access Token Secret']

tw = twitter.Twitter(auth=twitter.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
    CONSUMER_KEY, CONSUMER_SECRET_KEY))

searchTweets = tw.search.tweets(q="株価")
print(searchTweets['text'])