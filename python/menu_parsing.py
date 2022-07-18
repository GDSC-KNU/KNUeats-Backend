import os
from dotenv import load_dotenv
import pymysql
load_dotenv()
db_host = os.environ.get('knueats_host')
db_user = os.environ.get('knueats_user')
db_password = os.environ.get('knueats_password')
excepts = ['사진','별점','대표','주문','없습니다'] # 메뉴 크롤링 한 텍스트중에서 필요없는것들 모아놓음
connect = pymysql.connect(host=db_host, user=db_user, password=db_password, db='sys', charset='utf8')
cur = connect.cursor()
sql = "select * from sys.restaurant" # restaurant 테이블에 저장된 menu 다 들고옴
insert_sql = 'insert into menu (id,restaurant_id,name,price) VALUES (%s, %s, %s, %s)'
cur.execute(query=sql)
datas = cur.fetchall()
count = 1
for data in datas:
    restaurant_id = data[0] # 가게 id가 menu에 있는 데이터의 외부키임
    if data[-3] is None: # 메뉴가 없는 경우
        pass
    else: # 메뉴가 있는 경우
        menu = data[-3].split('\n') # 메뉴가 파인트\n8,900원\n쿼터17,000원\n 형식으로 들어가 있어서 '\n' 기준으로 나눠줘야함=
        new_menu = []
        for content in menu:
            flag = 0
            for ex in excepts: # 쓰레기 데이터가 들어가 있는 경우 없애준다
                if ex in content:
                    flag = 1
                    break
            if flag == 0: # 메뉴,가격에 대한 정보인 경우
                new_menu.append(content)
        for k in range(0,len(new_menu),2):
            print(new_menu[k]+ ' : '+ new_menu[k+1])
            cur.execute(insert_sql,(count,restaurant_id,new_menu[k],new_menu[k+1])) # 짝수 index에는 메뉴, 홀수 index에는 가격이 들어있기 때문에 2개씩 묶어서 넣어준다
            count+=1
connect.commit()
connect.close()
print(count)