import os
from dotenv import load_dotenv
import pymysql
import requests, json

load_dotenv()
kakao_client =os.environ.get('kakao_client_key')
area = ['산격동','복현동','신암동','대현동']
school_door = ['북문','동문','정문','쪽문&서문']
def get_location(address):
    index = 0
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query='+address
    headers = {"Authorization": "KakaoAK "+kakao_client}
    api_json = json.loads(str(requests.get(url,headers=headers).text))
    if len(api_json['documents']) == 0:
        return [0.0,0.0]
    address = api_json['documents'][0]['address']
    crd = [float(address['y']), float(address['x'])]
    address_name = address['address_name'].split(' ')
    for k in range(len(area)):
        if address_name[2] == area[k]:
            index = k
    print(address_name)
    crd.append(index)
    print(crd)
    return crd

def change(text): # category들을 최대한 정리해주기 위해서 next의 형태로 바꿔줌
    prev = ['중국식','경양식','정종/대포집/소주방','식육(숯불구이)','호프/통닭','통닭(치킨)','김밥(도시락)','까페','출장조리','패밀리레스트랑','탕류(보신용)','뷔페식']
    next = ['중식','양식','주점','고기/구이','주점','치킨','분식','카페','기타','양식','한식','양식']
    for i in range(0,len(prev)):
        if text == prev[i]:
            return next[i]
    return text


sql = "INSERT INTO restaurant (id,name,description,tel,address,lat,lon,category,position) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
connect = pymysql.connect(host='127.0.0.1', user='root', password='ccp980924', db='knueats', charset='utf8')
cur = connect.cursor()
f = open("C:/knueats/daegu_stores_tel.csv", 'r',encoding='cp949')
search = [['북구','대현로'],['북구','경대로'],['북구','경진로'],['북구','대학로'],['동구','평화로']]
table = {}
count = 0
cnt = 0
category = {}
while True:
    line = f.readline()
    print(line)
    if line == "":
        break
    if count == 0:
        pass
    else:
        temp = line.split(',')
        code = temp[3].split(' ')
        for k in search:
            if code[0] == '"대구광역시' and code[1] == k[0] and k[1] in code[2]:
                print(temp)
                pos = temp[3].split('(')[0][1:]
                prev_pos = temp[5].split('번지')
                prev_pos = prev_pos[0][1:] + "번지"
                local_temp = get_location(pos)
                lat = local_temp[0]
                lon = local_temp[1]
                kind = temp[2][1:-1]
                kind = change(kind)
                category[kind] = category.get(kind,0) + 1
                # if lat != 0.0:
                #     door = local_temp[2]
                #     if temp[-1] == "":
                #         cur.execute(sql,(str(cnt),temp[0][1:-1]," ",temp[-1],pos,lat,lon,kind,school_door[door]))
                #     else:
                #         cur.execute(sql,(str(cnt),temp[0][1:-1]," ",temp[-1][1:-2],pos,lat,lon,kind,school_door[door]))
                #     cnt +=1
    count+=1
print(count)
connect.commit()
connect.close()
print(cnt)
print(category)