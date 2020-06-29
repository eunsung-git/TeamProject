from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from .forms import CustomUserChangeForm, ProfileForm, MultipleImageForm
from django.contrib.auth import update_session_auth_hash
from .models import Profile, Category, Closet
from django.http import JsonResponse
import pandas as pd
import os
from django.conf import settings
import re
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .color_dect import color_dect
from .weather import weather
from .shoppingmall import shoppingmall
import random

# class 추가 시 from . import class이름

# Create your views here.

def login(request):
    # if login-ing, return index
    if request.user.is_authenticated:
        return redirect('pages:login_sel')

    if request.method == 'POST':
        # user 검증 + login
        # 1. data를 form에 넣기
        form = AuthenticationForm(request, request.POST)
        # 2. 유효성 검사
        if form.is_valid():
            # 3. 유효하다면 login
            user = form.get_user()
            auth_login(request, user)
            # 4. login 결과 확인
            return redirect('pages:login_sel')

    else:
        # user 로그인 페이지 보여주기
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'pages/main.html', context)

def signup(request): 
    # if login-ing, return index
    if request.user.is_authenticated:
        return redirect('pages:login_sel')

    if request.method == "POST":
        # user 생성
        # 1. data를 form에 넣기
        form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        # 2. 유효성 검사
        if form.is_valid() and profile_form.is_valid():
            # 3. 유효하다면 data 저장
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # profile 생성
            # Profile.objects.create(user=user)
            # 3-1. 회원가입 후, 바로 로그인
            auth_login(request, user)
            # 4. 저장 결과 확인
            return redirect('pages:closet')

    else:
        # user 생성 form 보여주기
        form = UserCreationForm()
        # profile 생성 form 보여주기
        profile_form = ProfileForm()
    context = {
        'form': form,
        'profile_form': profile_form,
    }
    return render(request, 'pages/signup.html', context)


def clothes(request): # 옷 업로드
    if request.method == 'POST':
        form = MultipleImageForm(request.POST, request.FILES)
        if form.is_valid():
            category_id = request.POST.get('category')
            images = request.FILES.getlist('images')
            for image in images:
                color = color_dect(image, False)
                clothes = Closet.objects.create(
                                category_id=category_id,
                                image=image,
                                color=color,
                                user=request.user)

            return redirect('pages:closet')
    else:
        form = MultipleImageForm()    
    context = {
        'form': form, 
    }
    return render(request, 'pages/clothes.html', context)


def closet(request):  # 옷 업로드 확인
    clothes_list = Closet.objects.all()
    context = {
        'clothes_list': clothes_list,
    }
    return render(request, 'pages/closet.html', context)

def closet_delete(request, pk):  # POST
    user = request.user
    clothes = Closet.objects.get(pk=pk)

    if request.method == 'POST':
        clothes.delete()

    return redirect('pages:closet')

def login_sel(request): # GET
    # form(id,pw), profile(region, image) 받기
    user = request.user
    form = CustomUserChangeForm(request.POST, instance=user) # id, ps
    profile = request.user.profile
    profile_form = ProfileForm(request.POST, request.FILES, instance=profile) # region, gender, image
 
    context = {
        'form': form, 'profile_form': profile_form, 
    }
    return render(request, 'pages/login_sel.html', context)

def shoppingmall(request):
    item = request.GET.get('item')

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
    urllib.request.urlretrieve('http:'+item1_img_url, item+'1.jpg')

    item_1 = {'brand':item1_brand,'name':item1_name, 'link':item1_link,'price':item1_price.text.split()[0],'img_url':item1_img_url}
    item_1_list = list(item_1.values())
    
    item2 = soup.select_one('#searchList > li:nth-of-type(2) > div.li_inner')
    item2_info = item2.find('a')
    item2_link = item2_info['href']
    item2_name = item2_info['title']
    
    item2_brand = item2.find('p',{'class':'item_title'}).text
    item2_price = item2.find('p',{'class':'price'})
    
    item2_img_url = item2.find('img')['data-original']
    urllib.request.urlretrieve('http:'+item2_img_url,item+'2.jpg')

    item_2 = {'brand':item2_brand,'name':item2_name, 'link':item2_link,'price':item2_price.text.split()[0],'img_url':item2_img_url}
    item_2_list = list(item_2.values())
    
    brand1 = item_1_list[0]
    item1 = item_1_list[1]
    link1 = item_1_list[2]
    price1 = item_1_list[3]
    image1 = item_1_list[4]
    
    brand2 = item_2_list[0]
    item2 = item_2_list[1]
    link2 = item_2_list[2]
    price2 = item_2_list[3]
    image2 = item_2_list[4]

    return render({'brand1': brand1, 'item1': item1, 'link1': link1, 'price1': price1, 'image1': image1,
        'brand2': brand2, 'item2': item2, 'link2': link2, 'price2': price2, 'image2': image2})

def recom(request):  # GET
    # profile 받아오기 - region, gender, image 
    profile = request.user.profile
    # profile_form = ProfileForm(request.POST, request.FILES, instance=profile) 

    date = request.GET.get('date')
    region = request.user.profile.region
    gender = request.user.profile.gender

    weather_mor = weather(date, region)[0]
    weather_aft = weather(date, region)[1]
    temp_mor = weather(date, region)[2]
    temp_aft = weather(date, region)[4]

    temp = (temp_mor+temp_aft)/2

    # 추천 함수   .... 마지막에 '맨투맨','청바지',... 이런 식으로 item 나옴
    # recommendation(temp, gender, closet)  = items1(맨투맨), items2(청바지) 0
    # 그러면 추천받은 items 따 와서
 
    # shoppingmall()함수 수행
    # shoppingmall(item1(맨투맨))[0] - 맨투맨 첫번째 리스트
    # brand1 = shoppingmall(item1)[0][0]
    # name1 = shoppingmall(item1)[0][1]
    # url1 = shoppingmall(item1)[0][2]
    # price1 = shoppingmall(item1)[0][3]
    # image1 = shoppingmall(item1)[0][4] ...
    
    # brand2 = shoppingmall(item2)[0]
    # name2 = shoppingmall(item2)[1]
    # url2 = shoppingmall(item2)[2]
    # price2 = shoppingmall(item2)[3]
    # image2 = shoppingmall(item2)[4]....

    # 이런 식으로 상의, 하의, 신발 3개를 shoppingmall() 넣고 실행
    # 1~6 까지의 shoppingmall list 출력
     
    
    context = {
        'weather_mor': weather_mor, 'weather_aft': weather_aft, 
        'temp_mor': temp_mor, 'temp_aft': temp_aft, 
        # 옷 items 추가
        'brand1': brand1, 'name1': item1, 'link1': link1, 'price1': price1, 'image1': image1,
        'brand2': brand2, 'name2': item2, 'link2': link2, 'price2': price2, 'image2': image2, 
        'brand3': brand3, 'name3': item3, 'link3': link3, 'price3': price3, 'image3': image3,
        'brand4': brand4, 'name4': item4, 'link4': link4, 'price4': price4, 'image4': image4, 
        'brand5': brand5, 'name5': item5, 'link5': link5, 'price5': price5, 'image5': image5,
        'brand6': brand6, 'name6': item6, 'link6': link6, 'price6': price6, 'image6': image6, 
    }
    return render(request, 'pages/recom.html', context)

def non_sel(request): # GET
    context = {
    }
    return render(request, 'pages/non_sel.html', context)

def non_recom(request):  # GET
    # date, region, gender 받아옴
    date = request.GET.get('date')
    region = request.GET.get('region')
    gender = request.GET.get('gender')

    weather_mor = weather(date, region)[0]
    weather_aft = weather(date, region)[1]
    temp_mor = weather(date, region)[2]
    temp_aft = weather(date, region)[4]

    temp = (temp_mor+temp_aft)/2

    # 추천 함수   .... 마지막에 '맨투맨','청바지',... 이런 식으로 item 나옴
    # recommendation(temp, gender, 기본옷들)  = items1(맨투맨), items2(청바지) 이렇게 나옴
    # 그러면 추천받은 items 따 와서

    # shoppingmall()함수 수행
    # shoppingmall(item1(맨투맨))[0] - 맨투맨 첫번째 리스트
    # brand1 = shoppingmall(item1)[0][0]
    # name1 = shoppingmall(item1)[0][1]
    # url1 = shoppingmall(item1)[0][2]
    # price1 = shoppingmall(item1)[0][3]
    # image1 = shoppingmall(item1)[0][4] ...

    # 이런 식으로 상의, 하의, 신발  총 3개를 shoppingmall() 넣고 실행
    # 1~6 까지의 shoppingmall list 출력

    context = {
        'date': date, 'region': region, 'gender': gender, 
        'weather_mor': weather_mor, 'weather_aft': weather_aft, 'temp_mor': temp_mor, 'temp_aft': temp_aft,
        # 옷 items 추가
        'brand1': brand1, 'name1': item1, 'link1': link1, 'price1': price1, 'image1': image1,
        'brand2': brand2, 'name2': item2, 'link2': link2, 'price2': price2, 'image2': image2, 
        'brand3': brand3, 'name3': item3, 'link3': link3, 'price3': price3, 'image3': image3,
        'brand4': brand4, 'name4': item4, 'link4': link4, 'price4': price4, 'image4': image4, 
        'brand5': brand5, 'name5': item5, 'link5': link5, 'price5': price5, 'image5': image5,
        'brand6': brand6, 'name6': item6, 'link6': link6, 'price6': price6, 'image6': image6, 
    }
    return render(request, 'pages/non_recom.html', context)

def logout(request): # POST
    if request.method == 'POST':
        # logout
        auth_logout(request)
    return redirect('pages:main')

def delete(request):  #POST
    # if not login-ing, return index
    if not request.user.is_authenticated:
        return redirect('pages:main')

    # user 삭제
    if request.method == 'POST':
        request.user.delete()
    return redirect('pages:main')

def edit(request):
    user = request.user

    if request.method == 'POST':
        # user update
        # 1. data를 form에 넣기
        form = CustomUserChangeForm(request.POST, instance=user)
        # 2. 유효성 검사
        if form.is_valid():
            # 3. 유효하다면, 저장
            form.save()
            # 4. update 결과 페이지
            return redirect('pages:main')
    else:
        # update form 보여주기
        form = CustomUserChangeForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'pages/edit.html', context)

def password(request):
    user = request.user
    if request.method == 'POST':
        # password 변경
        # 1. data에 form 넣기
        form = PasswordChangeForm(user, request.POST)
        # 2. 유효성 검사
        if form.is_valid():
            # 3. 유효하다면, 저장
            user = form.save()
            # 3-1. 저장 후, login 세션 유지
            update_session_auth_hash(request, user)
            # 4. 보내기
            return redirect('pages:edit')
    else:
        # password update form 보여주기
        form = PasswordChangeForm(user)
    context = {
        'form': form,
    }
    return render(request, 'pages/password.html', context)

def weather(request):
    date = request.GET.get('date')
    region = request.GET.get('region')

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

    lists = []
    icon = soup.select(' .date_info .point_time .ico_state2')
    for i,j in enumerate(icon) :
        if i>1:
            break
        lists.append(j.get('class')[1])

    cel = soup.select('li.date_info > dl > dd > span')
    for c,d in enumerate(cel) :
        if c>2:
            break
        lists.append(d.get_text())
    
    weather_mor = lists[0]
    weather_aft = lists[1]
    temp_mor = lists[2]
    temp_aft = lists[4]

    return render({'weather_mor': weather_mor, 'weather_aft': weather_aft,
                    'temp_mor': temp_mor, 'temp_aft': temp_aft})

def search_region(request):  # non_sel에서 
    dong = request.GET.get('dong')
    juso = pd.read_excel(os.path.join(settings.BASE_DIR, 'juso.xlsx'), sheet_name = '최종 업데이트 파일(2020404)')
    juso = juso.iloc[:,2:5]
    
    jibun = juso[juso['3단계']== dong]
    jibuns = jibun.to_numpy().tolist()

    return JsonResponse({'jibuns': jibuns})

def tip_link(request):
    item = request.GET.get('item')
    gender = request.GET.get('gender')

    df = pd.read_excel(os.path.join(settings.BASE_DIR, '팁.xlsx'))
    df = df[['category', 'gender', 'url','image_url']] 
    
    youtube = df.loc[(df['category']==item) & (df['gender']==gender), ['url','image_url']]
    youtube = youtube.values.tolist()
    youtube  = random.choice(youtube)
    
    return youtube
#     tip_link = youtube[0]
#     tip_thumbnail = youtube[1]

def tips(request):
    gender = request.user.profile.gender

    # 추천함수로부터 상의, 하의, 신발, 아우터 items 받아옴
    # tip_link(item1, gender)[0]  -> tip_link1
    # tip_link(item1, gender)[1]  -> tip_thumbnail1
    # tip_link(item2, gender)[0]  -> tip_link2
    # tip_link(item2, gender)[1]  -> tip_thumbnail2
    # tip_link(item3, gender)[0]  -> tip_link3
    # tip_link(item3, gender)[1]  -> tip_thumbnail3
    # tip_link(item4, gender)[0]  -> tip_link4
    # tip_link(item4, gender)[1]  -> tip_thumbnail4

    context = {
        'tip_link1': tip_link1, 'tip_thumbnail1': tip_thumbnail1,
        'tip_link2': tip_link2, 'tip_thumbnail2': tip_thumbnail2,
        'tip_link3': tip_link3, 'tip_thumbnail3': tip_thumbnail3,
        'tip_link4': tip_link4, 'tip_thumbnail4': tip_thumbnail4,
    }
    return render(request, 'pages/tips.html', context)

def profile_detail(request):
    # 1:n - user.comment_set / comment.user
    # 1:1 - user.profile / profile.user
    profile = request.user.profile
    context = {
        'profile': profile,
    }
    return render(request, 'pages/profile_detail.html', context)

def profile_edit(request):
    # 1. 현재 로그인된 profile 가져오기
    profile = request.user.profile
    if request.method == 'POST':
        # profile update
        # 1.data를 form에 넣기
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        # 2. 유효성 검사
        if form.is_valid():
            # 3. 저장
            form.save()
            # 4. 확인 페이지 안내
            return redirect('pages:profile_detail')
     
    else:
        # 2. form에 profile 넣기
        form =  ProfileForm(instance=profile)
    context = {
        'form': form,
    }
    return render(request, 'pages/profile_edit.html', context)
