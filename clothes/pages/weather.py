import re
import requests
from bs4 import BeautifulSoup

def weather(date, region):
    api_key = '%2FJgRrmm9JXaictz6llfBiClpFH5LGECjqZivf5V4Y5HwPgZLMmP38Ho6nqNdwp%2B%2B5z2qvJG6FeelYhnTh9yV%2Bg%3D%3D'
    pageNo = 1
    numOfRows = 10
    
    pat = re.findall('[a-zA-Z0-9_]+', date)
    base_date = ''.join(pat)
    
    nx = 55
    ny = 127

    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst'
    queryParams = '?' + 'ServiceKey='+api_key + '&pageNo='+str(pageNo) + '&numOfRows='+str(numOfRows) + '&dataType=JSON' + '&base_date='+str(base_date)+ '&base_time=1400'+ '&nx='+str(nx) + '&ny='+str(ny)

    response = requests.get(url + queryParams)
    data = response.json()
    
    regions = region.split(' ')
    do = regions[0]
    si = regions[1]
    dong = regions[2]

    source = requests.get('https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+do+si+dong+'날씨').text

    soup = BeautifulSoup(source, 'html.parser')

    # 날씨 아이콘 출력
    lists = []
    icon = soup.select(' .date_info .point_time .ico_state2')
    for i,j in enumerate(icon) :
        if i>1:
            break
        lists.append(j.get('class')[1])

    # 최저/최고 기온 출력
    cel = soup.select('li.date_info > dl > dd > span')
    for c,d in enumerate(cel) :
        if c>2:
            break
        lists.append(d.get_text())
        
    # weather_mor = lists[0]
    # weather_aft = lists[1]
    # temp_mor = lists[2]
    # temp_aft = lists[4]
    return  lists