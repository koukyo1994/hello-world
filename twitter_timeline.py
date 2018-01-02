import yaml
import twitter

with open("twitter_keys.yml", "r") as f:
    data = yaml.load(f)

CONSUMER_KEY = data['Consumer Key']
CONSUMER_SECRET_KEY = data['Consumer Secret']
ACCESS_TOKEN = data['Access Token']
ACCESS_TOKEN_SECRET = data['Access Token Secret']

tw = twitter.Twitter(auth=twitter.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
    CONSUMER_KEY, CONSUMER_SECRET_KEY))

timelines = tw.statuses.home_timeline()
for timeline in timelines:
    tl = '({id}) [{username}]: {text}'.format(
        id=timeline['id'], username=timeline['user']['name'], 
        text=timeline['text']
    )
    print(tl)