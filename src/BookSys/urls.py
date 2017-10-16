"""BookSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
# from django.contrib import admin
#
from django.views import static
from Book import views

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
    
    # static url
    url(r'^image/(?P<path>.*)$', static.serve,
        {'document_root': os.path.join(BASE_DIR, 'material', 'image')}, name='image'),
#     url(r'^jquery/(?P<path>.*)$', static.serve,
#         {'dcoument_root': os.path.join(BASE_DIR, 'ex-dep', 'jquery')}, name='jquery'),
#     url(r'^bootstrap/(?P<path>.*)$', static.serve,
#         {'document_root': os.path.join(BASE_DIR, 'ex-dep', 'bootstrap')}, name='bootstrap'),
    
    # view url
    url(r'^$', views.home, name='home'),
    url(r'^index/$', views.index, name='index'),
    url(r'^add_author/$', views.add_author, name='add_author'),
    url(r'^add_book/$', views.add_book, name='add_book'),
    url(r'^delete_book/$', views.delete_book, name='delete_book'),
    url(r'^get_book_detail/$', views.get_book_detail, name='get_book_detail'),
    url(r'^change_book_info/$', views.change_book_info, name='change_book_info'),
    url(r'^change_author_info/$', views.change_author_info, name='change_author_info'),
    url(r'^change_book_author/$', views.change_book_author, name='change_book_author'),
    url(r'^query_by_author_id_or_name/$', views.query_by_author_id_or_name, name='query_by_author_id_or_name'),
    url(r'^query_book_by_page/$', views.query_book_by_page, name='query_book_by_page'),
    url(r'^get_help_text/$', views.get_help_text, name='get_help_text'),
]
