import os
import time
from unicodedata import category
from dotenv import load_dotenv
import pymysql
import requests
exceptions = ['패션','캐주얼웨어','쇼핑','유통','오락시설','시설','건물','생활','편의','안경원,','주유소']
example = ['햄버거','샌드위치','피자','오뎅','꼬치','육류','브런치']
example_next = ['양식','양식','양식','일식','일식','한식','양식']

load_dotenv()
client_id =os.environ.get('client_naver_id')
client_secret = os.environ.get('client_naver_secret')
db_host = os.environ.get('knueats_host')
db_user = os.environ.get('knueats_user')
db_password = os.environ.get('knueats_password')
table = {}
req_header = {
    'X-Naver-Client-Id' : client_id,
    'X-Naver-Client-Secret' : client_secret 
}
connect = pymysql.connect(host=db_host, user=db_user, password=db_password, db='sys', charset='utf8')
cur = connect.cursor()
sql = "select * from sys.restaurant"
update_sql = "UPDATE restaurant SET category=%s WHERE id=%s"
menusql = "INSERT INTO menu (id,restaurant_id,name) VALUES (%s, %s, %s)"
cur.execute(query=sql)
data = cur.fetchall()
cnt = 1
for k in data:
    count = k[0]
    enctext = '산격동 '+k[1]
    url = 'https://openapi.naver.com/v1/search/local.json?query='+enctext+'&display=5&start=1&sort=random'
    req = requests.get(url,headers=req_header)
    data = req.json()
    if data['total'] == 0:
        pass
    else:
        print(data['items'][0]['category'])
        menu = data['items'][0]['category'].split('>')
        if len(menu) == 1:
            pass
        else:
            if menu[0] == '음식점':
                categorys = menu[1].split(',')
                for i in categorys:
                    flag = 0
                    for o in range(len(example)):
                        if i == example[o]:
                            table[example_next[o]] =  table.get(example_next[o],0) + 1
                            # cur.execute(menusql,(cnt,count,example_next[o]))
                            cur.execute(update_sql,(example_next[o],count))
                            cnt+=1
                            flag = 1
                            break
                    if flag == 0:
                        table[i] =  table.get(i,0) + 1
                        # cur.execute(menusql,(cnt,count,i))
                        cur.execute(update_sql,(i,count))
                        cnt+=1
            else:
                if menu[0] in exceptions:
                    pass
                else:
                    for i in menu[0].split(','):
                        flag2 = 0
                        for o in range(len(example)):
                            if i == example[o]:
                                table[example_next[o]] = table.get(example_next[o],0) + 1
                                # cur.execute(menusql,(cnt,count,example_next[o]))
                                cur.execute(update_sql,(example_next[o],count))
                                flag2 = 1
                                cnt+=1
                                break
                        if flag2 == 0:
                            table[i] =  table.get(i,0) + 1
                            # cur.execute(menusql,(cnt,count,i))
                            cur.execute(update_sql,(i,count))
                            cnt+=1
    time.sleep(0.11)
connect.commit()
connect.close()
print(table)