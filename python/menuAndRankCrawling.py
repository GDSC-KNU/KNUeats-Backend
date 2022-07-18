import os
import time
from dotenv import load_dotenv
import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
f = open('C:/knueats/menus.csv','w')
driver = webdriver.Chrome("C:/Program Files/chromedriver/chromedriver")
def menu(data): # 메뉴 크롤링
    driver.get("https://map.naver.com/v5/search/"+data) # 검색창에 가게이름 입력
    time.sleep(3)
    driver.implicitly_wait(3)
    # iframes = driver.find_elements_by_css_selector('iframe') # 창에 있는 모든 iframe 출력
    # for iframe in iframes:
    #     print(iframe.get_attribute('id'))
    driver.switch_to.frame('searchIframe') #  검색하고나서 가게정보창이 바로 안뜨는 경우 고려해서 무조건 맨위에 가게 링크 클릭하게 설정
    driver.implicitly_wait(3)
    temp = driver.find_element_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul') # 메뉴표에 있는 텍스트 모두 들고옴(개발자 도구에서 그때그때 xpath 복사해서 들고오는게 좋다)
    driver.implicitly_wait(20) # selenium에서 가끔씩 태그 시간내에 못찾는 경우 때문에 일부러 길게 설정해놓음
    button = temp.find_elements_by_tag_name('a')
    driver.implicitly_wait(20)
    if '이미지수' in button[0].text or button[0].text == '': # 가게 정보에 사진이 있는경우
        button[1].send_keys(Keys.ENTER) 
    else: # 사진이 없는 경우
        button[0].send_keys(Keys.ENTER)
    driver.implicitly_wait(3)
    time.sleep(3)
    driver.switch_to.default_content()# frame이 이상하게 넘어가는 경우 방지를 위해 원래 frame으로 변경한 후에 이동
    driver.switch_to.frame('entryIframe') # 메뉴정보가 entryIframe에 있기 때문에 frame 변경함
    driver.implicitly_wait(2)
    # time.sleep(3)
    start = driver.find_elements_by_class_name('_3ak_I') # 배달의 민족에서 제공하는 메뉴가 랜더링 되어 있는 경우
    if len(start) == 0: # 가게에서 직접 제공하는 메뉴가 랜더링 되어 있는 경우
        start = driver.find_elements_by_class_name('V1UmJ')
    if len(start) == 0: # 메뉴가 없는 경우
        print('메뉴가 없습니다')
        return -1
    return start[0].text

def rank(inputs):
    out = []
    driver.get("https://map.naver.com/v5/search/"+data) # 검색창에 가게이름 입력
    time.sleep(3)
    driver.implicitly_wait(3)
    # iframes = driver.find_elements_by_css_selector('iframe') # 창에 있는 모든 iframe 출력
    # for iframe in iframes:
    #     print(iframe.get_attribute('id'))
    driver.switch_to.frame('searchIframe') #  검색하고나서 가게정보창이 바로 안뜨는 경우 고려해서 무조건 맨위에 가게 링크 클릭하게 설정
    driver.implicitly_wait(3)
    temp = driver.find_element_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul') # 메뉴표에 있는 텍스트 모두 들고옴(개발자 도구에서 그때그때 xpath 복사해서 들고오는게 좋다)
    driver.implicitly_wait(20)
    button = temp.find_elements_by_tag_name('a')
    driver.implicitly_wait(20)
    if '이미지수' in button[0].text or button[0].text == '': # 가게 정보에 사진이 있는 경우
        button[1].send_keys(Keys.ENTER) 
    else: # 사진이 없는 경우
        button[0].send_keys(Keys.ENTER)
    driver.implicitly_wait(3)
    time.sleep(3)
    driver.switch_to.default_content()
    driver.switch_to.frame('entryIframe')
    driver.implicitly_wait(2)
    review = driver.find_element_by_css_selector('#app-root > div > div > div > div.place_section.GCwOh > div._3uUKd._2z4r0 > div._20Ivz') 
    # xpath는 가게마다 다르게 설정되어 있었기 때문에 css selector를 이용해서 review text가 있는 tag에 접근
    review_text = review.find_elements_by_tag_name('span') #span태그 안에서 별 규칙성을 찾지 못해서 span태그안에 별점, 리뷰 텍스트 정보가 들어가 있기 때문에 span에 있는거 모두 들고오기로 했음.
    for i in review_text:
        out.append(i.text) # parsing하기 쉽게 배열에 넣어놓음
    rank_report = 0.0
    review_report = 0
    print(out)
    if len(out) == 0:
        pass
    else:
        if '별점' in out[0]: # 별점이 존재하는 경우
            rank_report = float(out[0].split('\n')[1].split('/')[0]) # 별점을 실수형으로 바꿔서 담아둔다
            if len(out) >3 and '리뷰' in out[3]: # 리뷰가 방문자리뷰, 사용자리뷰 2개가 있는데 방문자, 사용자리뷰가 둘다 있는 경우
                out[2] = out[2].split(' ')[1].replace(',','') # [방문자리뷰,200] 이런 형태로 있는 데이터를 200만 가져오도록 parsing
                out[3] = out[3].split(' ')[1].replace(',','') # [사용자리뷰,50] 형태의 데이터를 50만 가져오도록 parsing
                review_report = int(out[2]) + int(out[3]) # 두 리뷰를 더해준다.
            else:
                out[2] = out[2].split(' ')[1].replace(',','') # 방문자리뷰만 있는 경우
                review_report = int(out[2])
        else: # 별점이 존재하지 않는 경우
            if len(out) < 2: # 방문자리뷰만 있는 경우 또는 사용자리뷰만 있는 경우
                out[0] = out[0].split(' ')[1].replace(',','')
                review_report = int(out[0])
            else: # 방문자리뷰, 사용자리뷰 둘다 있는 경우
                out[0] = out[0].split(' ')[1].replace(',','')
                out[1] = out[1].split(' ')[1].replace(',','')
                review_report = int(out[0]) + int(out[1]) # 리뷰 더해준다
    output = (rank_report,review_report) # 별점이랑 리뷰개수 담아서 return 해준다
    return output

load_dotenv() # id,secret은 naver api에서 등록한 후에 자기꺼 넣어주면 된다
client_id =os.environ.get('client_naver_id') # 디비에 들어가 있는 가게정보가 네이버 검색에도 뜨는지 확인해보기 위해서 naver api를 이용해서 검색하기 위해서 사용했음
client_secret = os.environ.get('client_naver_secret')
db_host = os.environ.get('knueats_host') # 디비도 자기꺼 사용하면 된다
db_user = os.environ.get('knueats_user')
db_password = os.environ.get('knueats_password')
req_header = {
    'X-Naver-Client-Id' : client_id,
    'X-Naver-Client-Secret' : client_secret 
}
table = {}
school = ['경대','경북대'] # 가끔씩 경대점/경북대점이 가게이름에 들어간 가게는 검색이 안되는 경우가 있어서 그 경우에는 동네이름 안넣어주도록 하기 위해서 넣어놨음
connect = pymysql.connect(host=db_host, user=db_user, password=db_password, db='sys', charset='utf8') # 디비 연결
cur = connect.cursor()
sql = "select * from sys.restaurant" # restaurant 테이블 다 들고오기 위한 sql
update_sql = "UPDATE restaurant SET menu=%s WHERE id=%s" # menu를 일단 추가해둔 다음에 따로 parsing해서 menu table에 따로 저장한다.
update_rank_sql = "UPDATE restaurant SET score=%s,review=%s WHERE id=%s" # 별점과 리뷰를 저장하기 위한 sql
cur.execute(query=sql)
data = cur.fetchall()
for k in data: # 데이터 다 검색해서 메뉴,별점&리뷰 있으면 넣어주고 아니면 pass
    enctext = '산격동 '+k[1] # 찾고 싶은 가게 동네 + 가게 이름하면 맨위에 바로 나옴..
    for texts in school: # 경북대점/경대점이 있으면 동네이름 안붙여줌
        if texts in k[1]:
            enctext = k[1]
    count = k[0]
    url = 'https://openapi.naver.com/v1/search/local.json?query='+enctext+'&display=5&start=1&sort=random' # 네이버 검색 api로 검색해서 나오는게 있는 경우에만 크롤링 하게 하기 위해 설정
    req = requests.get(url,headers=req_header)
    data = req.json()
    if data['total'] == 0: # 검색한 데이터가 없는 경우 -> 가게가 없어진 경우
        pass
    else: # 검색한 결과가 있는 경우
        out_rank,out_review = rank(enctext) # 별점, 리뷰 크롤링한거 들고온다
        out_rank *= out_review # 리뷰를 입력할 수 있기 때문에 새로운 리뷰가 들어오면 별점을 조정해주기 위해 별점 * 리뷰수로 저장해놓고 랜더링할때는 별점/리뷰수의 형태로 보여주기로 했다.
        cur.execute(update_rank_sql, (out_rank,out_review,count))
        menus = menu(enctext) # 메뉴 크롤링한거 들고온다
        if menus != -1: # 크롤링한 메뉴가 있는 경우
            line = menus.split('\n') # 나중에 parsing할때를 위해서 메뉴말고 어떤 텍스트가 들어가는지 확인해보기 위해서 만들어놓음
            table[count] = line
            cur.execute(update_sql, (menus,count)) # 디비에 수정해서 넣어준다
        else: # 크롤링한 메뉴가 없는 경우
            cur.execute(update_sql, ('제공된 정보가 없습니다.',count))
        connect.commit() # 가끔씩 중간에 오류 터지는거 생각해서 하나하고 넣어준다
    time.sleep(0.11) # naver 검색 api는 1초에 10회이상 request가 발생하면 오류나도록 설정돼있어서 1초에 9번 request하게 설정해놓음
print(table)
connect.commit()
connect.close()
driver.close()
    
