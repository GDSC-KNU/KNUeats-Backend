
import os
from dotenv import load_dotenv
import pymysql

load_dotenv()
db_host = os.environ.get('knueats_host')
db_user = os.environ.get('knueats_user')
db_password = os.environ.get('knueats_password')
door_area = ['산격동','복현동','신암동','대현동']
school_door = ['북문','동문','정문','쪽문&서문']
count = 0
sql = "INSERT INTO restaurant (id,name,description,tel,address,lat,lon,category,location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)" # 처음에 디비를 구성할때 스키마에 맞게 데이터를 넣어주기 위함
connect = pymysql.connect(host=db_host, user=db_user, password=db_password, db='sys', charset='utf8')
cur = connect.cursor()
f= open('C:/knueats/temp_store.csv', 'r',encoding='UTF8') # 대구광역시 북구에서 제공하는 식당 csv파일
search = [['북구','대현로'],['북구','경대로'],['북구','경진로'],['북구','대학로'],['동구','평화로']] # 학교주위에 있는 도로명으로 식당 가져옴
while True:
    line = f.readline()
    if line == "":
        break
    if count == 0:
        count+=1
        pass
    else:
        temp = line.split('#') # 가게 하나 정보 (데이터 내에','나 '\t'가 이상하게 들어가 있어서 '#'를 구분문자로 설정해서 데이터를 새로 만들어놨다).
        local = temp[9].split(',')[0] #도로명주소 들고옴
        code = local.split('(') #도로명주소(동)으로 구성된것을 도로명주소만 떼어내기 위해서 사용
        areas = code[0].split(' ') # 도로명 주소를 시/구/로 단위로 떼어냄
        print(areas)
        if len(areas) == 1:
            pass
        else:
            for k in search:
                if k[1] in areas[2]: # 학교주위에 있는 도로명인 경우
                    door_code = temp[7].split(' ')[2] # 옛날 주소로 어디 문이 더 가까운지 판단하기 위해 사용
                    door = ""
                    for i in range(len(door_area)): # 어디문에 가까운지 결정
                        if door_code == door_area[i]:
                            door = school_door[i]
                    tel = temp[5] # 식당 번호
                    lon = temp[11] # 위도
                    lat = temp[12] # 경도
                    menu = temp[13] # 메뉴(임시) 나중에 크롤링으로 대체
                    description = temp[14] # 운영시간과 같은 세부정보
                    if temp[10] == "N": # 폐업한 경우
                        pass
                    else:
                        cur.execute(sql,(str(count),temp[0],temp[-1],tel,code[0],lat,lon,menu,door)) # 디비에 넣어준다
                        count+=1
connect.commit()
connect.close()                   
print(count)