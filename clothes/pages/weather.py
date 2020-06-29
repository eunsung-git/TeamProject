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

    # 서울특별시+종로구+청운효자동
    source = requests.get('https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='+do+si+dong+'날씨').text

    # category : PTY 0, REH 76, RN1 0, T1H 20.5, UUU -0.1, VEC 23, VVV -0.4, WSD 0.5

    soup = BeautifulSoup(source, 'html.parser')

    # ws1 : 해, ws5 : 구름많음, ws7:흐림, ws9 : 비, ws22 : 흐리고 가끔 비

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