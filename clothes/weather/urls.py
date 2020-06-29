"""weather URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from pages import views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

app_name = 'pages'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('', lambda r: redirect('pages:login'), name='root'),
 
    # mainpage + 로그인
    # path('', views.login, name='login'), 

    # # 추천 결과_회원
    # path('recom/', views.recom, name='recom'),

    # # 추천 결과_비회원
    # path('non_recom/', views.non_recom, name='non_recom'),

    # # 회원가입 폼
    # path('signup/', views.signup, name='signup'),
    
    # # 로그아웃
    # path('logout/', views.logout, name='logout'),

    # # 로그인 후 옵션 선택
    # path('login_sel/', views.login_sel, name='login_sel'),

    # # 비회원 옵션 선택
    # path('non_sel/', views.non_sel, name='non_sel'),

    # # 팝업창
    # path('recom/tips/', views.tips, name='tips'),

    # # 회원 정보 수정
    # path('edit/', views.edit, name='edit'),

    # # 회원 탈퇴
    # path('delete/', views.delete, name='delete'),

    # # password 수정
    # path('password/', views.password, name='password'),

    # path('search_region/', views.search_region, name='search_region'),
    # # path('weather/', views.weather, name='weather'),

    # # profile - Read
    # path('profile/', views.profile_detail, name='profile_detail'),
    # # profile - update
    # path('profile/edit/', views.profile_edit, name='profile_edit'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

