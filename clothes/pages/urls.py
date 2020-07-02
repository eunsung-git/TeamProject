from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

app_name = 'pages'

urlpatterns = [
    # mainpage + 로그인
    path('', views.login, name='login'), 

    # 추천 결과_회원
    path('recom/', views.recom, name='recom'),

    # 추천 결과_비회원
    path('non_recom/', views.non_recom, name='non_recom'),

    # 회원가입 폼
    path('signup/', views.signup, name='signup'),

    # 옷 업로드
    path('clothes/', views.clothes, name='clothes'),

    # 업로드된 옷 확인
    path('closet/', views.closet, name='closet'),

    # 업로드된 옷 삭제
    path('closet/<int:pk>/delete/', views.closet_delete, name='closet_delete'),
    
    # 로그아웃
    path('logout/', views.logout, name='logout'),

    # 로그인 후 옵션 선택
    path('login_sel/', views.login_sel, name='login_sel'),

    # 비회원 옵션 선택
    path('non_sel/', views.non_sel, name='non_sel'),

    # 팁
    # path('recom/tips/', views.tips, name='tips'),

    # 회원 정보 수정
    path('edit/', views.edit, name='edit'),

    # 회원 탈퇴
    path('delete/', views.delete, name='delete'),

    # password 수정
    path('password/', views.password, name='password'),

    path('', lambda r: redirect('pages:login'), name='root'),

    path('search_region/', views.search_region, name='search_region'),
    # path('weather/', views.weather, name='weather'),

    # profile - Read
    path('profile/', views.profile_detail, name='profile_detail'),
    # profile - update
    path('profile/edit/', views.profile_edit, name='profile_edit'),

]