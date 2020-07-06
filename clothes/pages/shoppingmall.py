import requests
import urllib.request
from bs4 import BeautifulSoup
from django.conf import settings


def shoppingmall(item):
    result = []

    url = 'https://search.musinsa.com/search/musinsa/?q={}'.format(item)
    resp = requests.get(url)
    
    soup = BeautifulSoup(resp.text)
    
    item1 = soup.select_one('#searchList > li:nth-of-type(1) > div.li_inner')
    item1_info = item1.find('a')
    item1_link = item1_info['href']
    item1_name = item1_info['title']
    
    item1_brand = item1.find('p',{'class':'item_title'}).text
    item1_price = item1.find('p',{'class':'price'})
    
    item1_img_url = item1.find('img')['data-original']
    # urllib.request.urlretrieve('http:'+item1_img_url, f'{settings.BASE_DIR}/crawling/'+item+'1.jpg')

    item_1 = {'brand':item1_brand,'name':item1_name, 'link':item1_link,'price':item1_price.text.split()[0],'img_url':item1_img_url}
    item_1_list = list(item_1.values())
    
    item2 = soup.select_one('#searchList > li:nth-of-type(2) > div.li_inner')
    item2_info = item2.find('a')
    item2_link = item2_info['href']
    item2_name = item2_info['title']
    
    item2_brand = item2.find('p',{'class':'item_title'}).text
    item2_price = item2.find('p',{'class':'price'})
    
    item2_img_url = item2.find('img')['data-original']
    # urllib.request.urlretrieve('http:'+item2_img_url, f'{settings.BASE_DIR}/crawling/'+item+'2.jpg')

    item_2 = {'brand':item2_brand,'name':item2_name, 'link':item2_link,'price':item2_price.text.split()[0],'img_url':item2_img_url}
    item_2_list = list(item_2.values())
    
    return item_1_list, item_2_list
    # return render({'brand1': brand1, 'item1': item1, 'link1': link1, 'price1': price1, 'image1': image1,
    #     'brand2': brand2, 'item2': item2, 'link2': link2, 'price2': price2, 'image2': image2})