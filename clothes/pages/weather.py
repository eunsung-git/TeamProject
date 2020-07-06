import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def weather(date, region):
    pat = re.findall('[a-zA-Z0-9_]+', date)
    base_date = ''.join(pat)

    regions = region.split(' ')
    do = regions[0]
    si = regions[1]
    dong = regions[2]

    source = requests.get('https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+do+si+dong+'날씨').text

    soup = BeautifulSoup(source, 'html.parser')

    today = datetime.today()
    period = datetime.strptime(base_date, '%Y%m%d') - today
    period = int(period.days) +1
    
    # 날씨 아이콘 출력
    lists = []
    icon = soup.select(' .date_info .point_time .ico_state2')
    for i,j in enumerate(icon) :
        if (i == period*2) or (i == period*2+1):
            lists.append(j.get('class')[1])
    
    # 최저/최고 기온 출력
    cel = soup.select('li.date_info > dl > dd > span')
    for c,d in enumerate(cel) :
        if (c == period*3) or (c == period*3+2):
            lists.append(d.get_text())
    
    # weather_mor = lists[0]
    # weather_aft = lists[1]
    # temp_mor = lists[2]
    # temp_aft = lists[4]
    return  lists