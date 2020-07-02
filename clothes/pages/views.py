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
from .color_match import color_match
from .recommendation import recommendation
from .recommendation2 import recommendation2
from .tip_link import tip_link
import random
from skimage import io

# class 추가 시 from . import class이름

# Create your views here.

top_list = ['후드티','반팔','민소매','맨투맨','니트','긴팔']
bottom_list = ['치마','청바지','슬렉스','면바지','반바지']
outer_list = ['코트','패딩','집업','자켓','가디건']
shoes_list = ['운동화','워커','구두','샌들']

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
                color = color_dect(image)
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

def recom(request):  # GET
    # profile 받아오기 - region, gender, image 
    profile = request.user.profile
    # profile_form = ProfileForm(request.POST, request.FILES, instance=profile) 

    date = request.GET.get('date')
    region = request.user.profile.region
    gender = request.user.profile.gender

    weather_mor = weather(date, region)[0]
    weather_aft = weather(date, region)[1]
    temp_mor = int(weather(date, region)[2])
    temp_aft = int(weather(date, region)[4])
    
    temp = (temp_mor+temp_aft)/2

    # user = request.user
    # closet = Closet.objects.filter(user=user)
    closet = request.user.closet_set.all()

    item_pk_list = recommendation(temp, gender, closet) # [1,2,3,4]
    
    # instance 
    items = []
    for pk in item_pk_list:
        items.append(Closet.objects.get(pk=pk))
    
    # category & image
    category_list = []  # 추천받은 옷 카테고리 
    image_list = []  # 추천받은 옷 images
    for item in items:
        category_list.append(item.category)
        image_list.append(item.image)

    
    shop_image_list = []  # 몰 옷 이미지
    brand_list = [] # 몰 브랜드 이름
    name_list = [] # 몰 옷 이름
    url_list = []  # 몰 옷 유알엘
    price_list = []  # 몰 옷 가격

    for item in category_list:
        for infor in shoppingmall(item.name):
            brand_list.append(infor[0])
            name_list.append(infor[1])
            url_list.append(infor[2])
            price_list.append(infor[3])
            shop_image_list.append(infor[4])
            
    # tips
    tip_url = []  # tip 주소들
    tip_thumbnail = []   # tip 썸네일
    tip_title = []   # tip title
    
    for item in category_list:
        tips = tip_link(item.name, gender)
        tip_url.append(tips[0])
        tip_thumbnail.append(tips[1])
        tip_title.append(tips[2])
    for image in image_list:
        # print(dir(image))
        print('-----')
        print(image.url)
        # print(image.path)
    
    context = {
        'weather_mor': weather_mor, 'weather_aft': weather_aft, 
        'temp_mor': temp_mor, 'temp_aft': temp_aft, 
        'items': items, 'category_list': category_list, 'image_list': image_list,
        'shop_image_list': shop_image_list, 'brand_list': brand_list, 
        'name_list': name_list, 'url_list': url_list, 'price_list': price_list,
        'tip_url': tip_url, 'tip_thumbnail': tip_thumbnail, 'tip_title': tip_title,
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
    temp_mor = int(weather(date, region)[2])
    temp_aft = int(weather(date, region)[4])

    temp = (temp_mor+temp_aft)/2
    
    closet = pd.DataFrame({
        'pk': list(range(24)),
        'category': ['가디건', '가죽자켓', '구두', '긴팔', '니트',
                     '맨투맨', '면바지', '민소매', '반바지', '반팔',
                     '부츠', '샌들', '셔츠', '슬렉스', '운동화', 
                     '워커', '원피스', '자켓', '집업', '청바지', 
                     '치마' , '코트', '패딩', '후드티'],
        'color': ['black']*24
    })
    
    item_pk_list = recommendation2(temp, gender, closet) # [1,2,3,4]
    
    # 추천 받은 옷 카테고리 
    category_list = []
    for pk in item_pk_list:
        category_list.append(closet['category'][pk])
    
    # 이미지 불러오기
    image_list = []
    for item in category_list:
        image_list.append('../static/samples/'+item+'.png')

    # 광고를 위한 변수
    shop_image_list = []  # 몰 옷 이미지
    brand_list = [] # 몰 브랜드 이름
    name_list = [] # 몰 옷 이름
    url_list = []  # 몰 옷 유알엘
    price_list = []  # 몰 옷 가격

    for item in category_list:
        for infor in shoppingmall(item):
            brand_list.append(infor[0])
            name_list.append(infor[1])
            url_list.append(infor[2])
            price_list.append(infor[3])
            shop_image_list.append(infor[4])
            
    # tips
    tip_url = []  # tip 주소들
    tip_thumbnail = [] # tip 썸네일
    tip_title = []   # tip title
    
    for item in category_list:
        tips = tip_link(item,gender)
        tip_url.append(tips[0])
        tip_thumbnail.append(tips[1])
        tip_title.append(tips[2])

    context = {
        'date': date, 'region': region, 'gender': gender, 
        'weather_mor': weather_mor, 'weather_aft': weather_aft, 'temp_mor': temp_mor, 'temp_aft': temp_aft,
        'category_list': category_list, 'image_list': image_list,
        'shop_image_list': shop_image_list, 'brand_list': brand_list, 
        'name_list': name_list, 'url_list': url_list, 'price_list': price_list,
        'tip_url': tip_url, 'tip_thumbnail': tip_thumbnail, 'tip_title': tip_title,
    }
    return render(request, 'pages/non_recom.html', context)

def logout(request): # POST
    if request.method == 'POST':
        # logout
        auth_logout(request)
    return redirect('pages:login')

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
            return redirect('pages:login')
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

def search_region(request):  # non_sel에서 
    dong = request.GET.get('dong')
    juso = pd.read_excel(os.path.join(settings.BASE_DIR, 'juso.xlsx'), sheet_name = '최종 업데이트 파일(2020404)')
    juso = juso.iloc[:,2:5]
    
    jibun = juso[juso['3단계']== dong]
    jibuns = jibun.to_numpy().tolist()

    return JsonResponse({'jibuns': jibuns})

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
