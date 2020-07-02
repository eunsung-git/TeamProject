import pandas as pd
import random
from .color_match import color_match

def recommendation(temp, gender, closet):
    # 날씨 분류
    if temp >= 17:
        if temp >= 23:
            if temp >= 27:
                weather_category = 'warm1'
            else:
                weather_category = 'warm2'
        else:
            if temp >= 20:
                weather_category = 'warm3'
            else:
                weather_category = 'warm4'
    else:
        if temp >= 10:
            if temp >= 12:
                weather_category = 'cool1'
            else:
                weather_category = 'cool2'
        else:
            if temp >= 6:
                weather_category = 'cool3'
            else:
                weather_category = 'cool4'
    
    # 날씨에 따른 옷 선택지
    if weather_category[:4] == 'warm':
        if weather_category == 'warm1':
            clothes_kind = {'상의':['민소매', '반팔'],
                            '하의':['반바지', '치마'],
                            '원피스':['원피스'],
                            '신발':['운동화', '샌들', '구두']}
        elif weather_category == 'warm2':
            clothes_kind = {'상의':['반팔'], 
                            '하의':['반바지', '면바지', '치마'],
                            '신발':['운동화', '워커']}
        elif weather_category == 'warm3':
            clothes_kind = {'상의':['긴팔', '후드티', '맨투맨'],
                            '하의':['면바지', '슬렉스', '청바지', '치마'],
                            '신발':['운동화', '워커']}
        else:
            clothes_kind = {'상의':['긴팔', '니트', '후드티', '맨투맨'],
                            '하의':['면바지', '청바지', '슬렉스', '치마'],
                            '원피스':['원피스'],
                            '신발':['운동화', '워커']}
    else:
        if weather_category == 'cool1':
            clothes_kind = {'상의':['셔츠', '긴팔'],
                            '하의':['면바지', '청바지', '슬렉스', '치마'],
                            '신발':['운동화', '워커'],
                            '아우터':['자켓', '가디건']}
        elif weather_category == 'cool2':
            clothes_kind = {'상의':['셔츠', '긴팔', '니트'],
                            '하의':['청바지', '치마'],
                            '신발':['운동화', '워커'], 
                            '아우터':['자켓', '집업']}
        elif weather_category == 'cool3':
            clothes_kind = {'상의':['셔츠', '긴팔', '니트'],
                            '하의':['면바지', '청바지', '슬렉스', '치마'],
                            '신발':['운동화', '부츠', '워커'], 
                            '아우터':['코트', '가죽자켓']}
        else:
            clothes_kind = {'상의':['셔츠', '긴팔', '니트'],
                            '하의':['면바지', '청바지', '슬렉스', '치마'],
                            '신발':['운동화', '부츠'],
                            '아우터':['코트', '패딩']}
    # 남성일 경우 여자 옷 제거
    if gender == '남성':
        if '원피스' in clothes_kind.keys():
            clothes_kind.pop('원피스', None)
        if '치마' in clothes_kind['하의']:
            clothes_kind['하의'] = [k for k in clothes_kind['하의'] if k != '치마']
    
    # 옷 선택지에 '원피스'가 있고 옷장에 '원피스'가 있을 경우, 원피스와 상하의 중에 random sample
    if '원피스' in clothes_kind.keys():
        if '원피스' in closet.category.values:
            choice = random.sample(['원피스', '상하의'], 1)[0]
        else:
            choice = ['상하의']
    else:
        choice = ['상하의']

    # 위의 선택에 따라 선택지 삭제
    kind = list(clothes_kind.keys())
    if choice == '원피스':
        kind.remove('상의')
        kind.remove('하의')
    else:
        if '원피스' in kind:
            kind.remove('원피스')
                
    # 옷 선택
    rot = True
    while rot:
        # 옷 random sample
        choices = []
        for k in kind:
            pk_list = closet.filter(category__name__in=clothes_kind[k]).values_list('id', flat=True)
            # pk_list = closet[[c in clothes_kind[k] for c in closet.category]].pk.values
            choice_pk = random.sample(list(pk_list), 1)
            choices.extend(choice_pk)
        
        # 색상 배치
        if choice == '원피스':
            rot = False
        else:
            c1 = closet.get(pk=choices[0]).color # black
            c2 = closet.get(pk=choices[1]).color # black
            # c2 = closet[closet.pk == choices[1]].color.values[0]
            rot = color_match(c1, c2)
            
    ### while 끝
    return choices