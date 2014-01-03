#import weibo as wb
from weibo import APIClient
import json

oauth_token='2.00N8wSuB05_4UJ6f4f7a6937VtKvvC'

client=APIClient()
client.set_access_token(oauth_token,0.0)


usr_timeline=client.friendships.followers.ids.get(uid=3242547294,count=5000)
#print usr_timeline['total_number']
f_timeline=open('user_followers.json','w')
json.dump(usr_timeline,f_timeline)
f_timeline.close()
