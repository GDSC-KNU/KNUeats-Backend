from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
array = []
inputs = ['산격동 배스킨라빈스대구경대북문점','에그드랍 경북대점','사군자민속촌','대현동 청춘토스트','서브웨이 경북대점']
driver = webdriver.Chrome("C:/Program Files/chromedriver/chromedriver")
for i in inputs:
    driver.get("https://map.naver.com/v5/search/"+i) # 검색창에 가게이름 입력
    time.sleep(3)
    driver.implicitly_wait(2)
    iframes = driver.find_elements_by_css_selector('iframe')
    for iframe in iframes: # 창에 있는 모든 iframe 출력
        print(iframe.get_attribute('id')) 
    driver.switch_to.frame('searchIframe') #  검색할때 가게 바로 안뜨느 경우 고려해서 무조건 맨위에 가게 링크 클릭하게 설정
    driver.implicitly_wait(2)
    temp = driver.find_elements_by_xpath('//*[@id="_pcmap_list_scroll_container"]/ul') # 메뉴표에 있는 텍스트 모두 들고옴(개발자 도구에서 그때그때 xpath 복사해서 들고오는게 좋다)
    button = temp[0].find_elements_by_tag_name('a')
    print(button[0].text)
    print(len(button[0].text))
    if '이미지수' in button[0].text: # 가게 정보에 사진개수가 2이상 있는경우
        button[1].send_keys(Keys.ENTER)
    elif button[0].text == '': # 사진이 하나 있는 경우
        button[1].send_keys(Keys.ENTER)
    else: # 사진이 없는 경우
        button[0].send_keys(Keys.ENTER)
    driver.implicitly_wait(2)
    time.sleep(3)
    driver.switch_to.default_content() # frame이 이상하게 넘어가는 경우 방지를 위해 원래 frame으로 변경한 후에 이동
    driver.switch_to.frame('entryIframe') # 메뉴정보가 entryIframe에 있기 때문에 frame 변경함
    driver.implicitly_wait(2)
    start = driver.find_elements_by_class_name('_3ak_I') # 배달의 민족에서 제공하는 메뉴가 랜더링 되어 있는 경우
    if len(start) == 0: # 가게에서 직접 제공하는 메뉴가 랜더링 되어 있는 경우
        start = driver.find_elements_by_class_name('V1UmJ')
    if len(start) == 0: # 메뉴가 없는 경우
        print('메뉴가 없습니다')
        pass
    array.append(start[0].text)
print(array)