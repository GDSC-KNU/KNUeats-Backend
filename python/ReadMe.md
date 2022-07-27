# Knueats-Data
- 공공데이터 api를 통해서 학교 주변에 있는 가게 기본정보를 가져옴

- 가게 이름을 통해서 naver map을 크롤링해 가게 메뉴,별점,리뷰등을 크롤링

## Database
#### Schema
```
restaurant(1)
{
	id : INT(primary key,not null,auto increment)
	name : VARCHAR(not null)
	description : VARCHAR
	tel : VARCHAR
	address : VARCHAR(not null)
	lat : VARCHAR(not null)
	lon : VARCHAR(not null)
	category : VARCHAR(not null)
	location : VARCHAR(null)
	score : FLOAT(0.0)
	review : INT(0)
}

menu(N)
{
	id : INT(not null,auto increment)
	restaurant_id : INT(foreign key-id)
	name : VARCHAR(not null)
	price : VARCHAR(not null) // ex) "12,000원"
}
```
#### Data source
- 대구광역시 등록음식점 현황

  https://www.data.go.kr/data/3056779/fileData.do?recommendDataYn=Y
- 대구광역시 북구 관광지 주변 음식점

  https://www.data.go.kr/data/15095875/fileData.do
#### Geocoding
공공데이터에 도로명주소만 명시되어 있고 위,경도는 표시되어 있지 않아서 위,경도를 저장해주기 위해서 사용했다.
- Kakao Local Api(도로명주소 -> 위,경도 변환)
  #### api document
  
  https://developers.kakao.com/docs/latest/ko/local/dev-guide#address-coord

other.py
```
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
    crd.append(index)
    return crd
```

## Data Crawling
- beautifulsoup와 selenium을 라이브러리를 이용해서 크롤링했다.

  selenium을 사용한 이유는 naver map에 iframe을 전환해줘야 했기 때문에 사용했다
- crawling url
  
  https://map.naver.com/v5/search/{restaurant}
  
  #### 검색한 가게가 있는지 확인
  공공데이터에서 받아온 가게가 실제로 영업하는지 확인하기 위해서 api를 사용했다.
  - naver search api
  
    https://openapi.naver.com/v1/search/local.json?query={restaurant}&display=5&start=1&sort=random
    
    #### api document
    
    https://developers.naver.com/docs/serviceapi/search/local/local.md#%EC%A7%80%EC%97%AD
  
  #### Menu crawling
  검색한 가게에 있는 메뉴 목록을 가져온다
  
  menu_crawling.py
  ```
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
  ```
  #### 별점&리뷰 crawling
  검색한 가게에 등록된 별점과 리뷰를 가져온다.
  
  rank.py
  ```
  def rank(data):
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
  ```
