#import weibo as wb
from weibo import APIClient
import json
import io
import os
from collections import *
from bitarray import *

n=10000000

def get_mod(num):
    return num%n

abit=bitarray(n)
abit.setall(False)
with open('succ.txt','r') as f:
    for line in f:
        abit[get_mod(int(line))]=True

start_id=1748122191
qu=deque()
qu.append(start_id)
with open('unfinish.txt','r') as f:
    for line in f:
        qu.append(int(line))

#magic token ^_^
oauth_token='2.00N8wSuB05_4UJ6f4f7a6937VtKvvC'
#'2.00y3jlGD05_4UJ6b923480c0zXKxQC'
client=APIClient()
client.set_access_token(oauth_token,0.0)

while qu:
    it=qu.popleft()
    if abit[get_mod(it)]:
        print '{0} is skipped for hash hitting'.format(it)
        continue
    print 'get {0} \'s info'.format(it)
    abit[get_mod(it)]=True
    if not os.path.exists(str(it)):
        os.mkdir(str(it))
    f_fr=open(str(it)+'/friends_ids.json','w')
    f_fl=open(str(it)+'/followers_ids.json','w')
    f_us=open(str(it)+'/users_show.json','w')
    f_timeline=open(str(it)+'/user_timeline.json','w')
    f_education=open(str(it)+'/education.json','w')
    f_basic=open(str(it)+'/basic.json','w')
    f_career=open(str(it)+'/career.json','w')
    try:
        cursor=0
        fr_num=0
        go_next=True
        friends_ids=[]
        while go_next:
            friends=client.friendships.friends.ids.get(uid=it,cursor=cursor,count=5000)
            cursor=friends['next_cursor']
            friends_ids=friends_ids+friends['ids']
            fr_num=friends['total_number']
            if cursor==0:
                go_next=False
        json.dump(friends_ids,f_fr)
        f_fr.close()

        cursor=0
        fl_num=0
        go_next=True
        followers_ids=[]
        while go_next:
            followers=client.friendships.followers.ids.get(uid=it,cursor=cursor,count=5000)
            cursor=followers['next_cursor']
            followers_ids=followers_ids+followers['ids']
            fl_num=followers['total_number']
            if cursor==0:
                go_next=False
        json.dump(followers_ids,f_fl)
        f_fl.close()
        if fr_num<10000:
            for i in friends_ids:
                qu.append(i)
        if fl_num<10000:
            for i in followers_ids:
                qu.append(i)
        page=1
        temp_num=0
        go_next=True
        status=[]
        while go_next:
            status_page=client.statuses.user_timeline.get(uid=it,count=100,page=page)
            total_num=status_page['total_number']
            status=status+status_page['statuses']
            temp_num=temp_num+100
            if total_num<=temp_num:
                go_next=False
        json.dump(status,f_timeline)
        f_timeline.close()
        users_show=client.users.show.get(uid=it)
        json.dump(users_show,f_us)
        f_us.close()
        education=client.account.profile.education.get(uid=it)
        json.dump(education,f_education)
        f_education.close()
        basic=client.account.profile.basic.get(uid=it)
        json.dump(basic,f_basic)
        f_basic.close()
        career=client.account.profile.career.get(uid=it)
        json.dump(career,f_career)
        f_career.close()
        f_succ=open('succ.txt','ab')
        f_succ.write(str(it)+'\n')
    except:
        print 'except happens'
        f_unfinish=open('unfinish.txt','w')
        for i in qu:
            f_unfinish.write(str(i)+'\n')
        f_unfinish.close()
    finally:
        f_fr.close()
        f_timeline.close()
        f_fl.close()
        f_us.close()
        f_education.close()
        f_basic.close()
        f_career.close()
