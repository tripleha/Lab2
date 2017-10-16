# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from Book.models import Author, Book
import os
import json
import re
import time
import traceback


# 路径准备
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HELP_DIR = os.path.join(BASE_DIR, 'material', 'help-text')


# 数据准备
author_item = ['author_id', 'name', 'age', 'country']

pattern_author_dict = {
    'author_id': r'^[1-9]{1}[0-9]{0,19}$',
    'name': r'^.{1,50}$',
    'age': r'^[0-9]{1,3}$',
    'country': r'^.{1,50}$',
}

book_item = ['isbn', 'title', 'author_id', 'publisher', 'publish_date', 'price']

pattern_book_dict = {
    'isbn': r'^[0-9]{13}$',
    'title': r'^.{1,50}$',
    'author_id': r'^[1-9]{1}[0-9]{0,19}$',
    'publisher': r'^.{1,50}$',
    'publish_date': r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
    'price': r'^([0-9]+\.[0-9]+|[0-9]+)$',
}

def save_html(data):
    return data.replace('<', '《').replace('>', '》')


# 功能函数
def check_date(date):
    try:
        time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False


def home(request):
    return render(request, 'home.html')


def index(request):
    return render(request, 'index.html')


def get_help_text(request):
    help_file = open(os.path.join(HELP_DIR, 'help.txt'), 'rb')
    help_put = map(lambda i: i.decode('gbk', 'ignore'), help_file.readlines())
    return HttpResponse(json.dumps(help_put), content_type='application/json')


def add_author(request):
    result = {
        'retcode': 10000,
        'errkey': "",
    }
    
    try:
        re_flag = True
        for i in xrange(len(author_item)):
            if not re.match(pattern_author_dict[author_item[i]], request.POST[author_item[i]]):
                result['retcode'] = 10003
                result['errkey'] = author_item[i]
                re_flag = False
                break
        if re_flag:
            check_set = Author.objects.filter(author_id=request.POST['author_id'])
            if check_set.exists():
                result['retcode'] = 10001
                re_flag = False
                
        if re_flag:
            Author.objects.create(
                author_id=request.POST['author_id'],
                name=save_html(request.POST['name']),
                age=int(request.POST['age']),
                country=save_html(request.POST['country'])
            )
            result['retcode'] = 0
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
    return HttpResponse(json.dumps(result), content_type='application/json')


def add_book(request):
    result = {
        'retcode': 10000,
        'errkey': "",
    }
    
    try:
        re_flag = True
        for i in xrange(len(book_item)):
            if not re.match(pattern_book_dict[book_item[i]], request.POST[book_item[i]]):
                result['retcode'] = 10003
                result['errkey'] = book_item[i]
                re_flag = False
                break
        if re_flag:
            if not check_date(request.POST['publish_date']):
                result['retcode'] = 10003
                result['errkey'] = "publish_date"
                re_flag = False
            
        if re_flag:
            check_set = Book.objects.filter(isbn=request.POST['isbn'])
            if check_set.exists():
                result['retcode'] = 10001
                re_flag = False
        if re_flag:
            author_set = Author.objects.filter(author_id=request.POST['author_id'])
            if not author_set.exists():
                result['retcode'] = 10002
                re_flag = False
                
        if re_flag:
            Book.objects.create(
                isbn=request.POST['isbn'],
                title=save_html(request.POST['title']),
                author=author_set[0],
                publisher=save_html(request.POST['publisher']),
                publish_date=request.POST['publish_date'],
                price=float(request.POST['price'])
            )
            result['retcode'] = 0
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
    return HttpResponse(json.dumps(result), content_type='application/json')


def delete_book(request):
    result = {
        'retcode': 10000,
        'errkey': "",
    }
    
    try:
        if not re.match(pattern_book_dict['isbn'], request.POST['isbn']):
            result['retcode'] = 10003
            result['errkey'] = "isbn"
        else:
            try:
                book_get = Book.objects.get(isbn=request.POST['isbn'])
                book_get.delete()
                result['retcode'] = 0
            except:
                result['retcode'] = 10001
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
    return HttpResponse(json.dumps(result), content_type='application/json')


def get_book_detail(request):
    result = {
        'retcode': 10000,
        'author': {},
        'book': {},
        'errkey': "",
    }
    
    try:
        if not re.match(pattern_book_dict['isbn'], request.POST['isbn']):
            result['retcode'] = 10003
            result['errkey'] = "isbn"
        else:
            book_set = Book.objects.filter(isbn=request.POST['isbn'])
            if book_set.exists():
                result['author'] = book_set[0].author.to_dict()
                result['book'] = book_set[0].to_dict()
                result['retcode'] = 0
            else:
                result['retcode'] = 10001
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
    return HttpResponse(json.dumps(result), content_type='application/json')


def change_book_info(request):
    result = {
        'retcode': 10000,
        'errkey': "",
    }
    
    try:
        re_flag = True
        for i in xrange(len(book_item)):
            if not re.match(pattern_book_dict[book_item[i]], request.POST[book_item[i]]):
                result['retcode'] = 10003
                result['errkey'] = book_item[i]
                re_flag = False
                break
        if re_flag:
            if not check_date(request.POST['publish_date']):
                result['retcode'] = 10003
                result['errkey'] = "publish_date"
                re_flag = False
                
        if re_flag:
            try:
                book_get = Book.objects.get(isbn=request.POST['isbn'])
                book_get.publisher = save_html(request.POST['publisher'])
                book_get.publish_date = request.POST['publish_date']
                book_get.price = float(request.POST['price'])
                book_get.save(update_fields=book_item[3:])
                result['retcode'] = 0
            except:
                result['retcode'] = 10001
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
    return HttpResponse(json.dumps(result), content_type='application/json')


def change_author_info(request):
    result = {
        'retcode': 10000,
        'errkey': "",
    }
    
    try:
        re_flag = True
        for i in xrange(len(author_item)):
            if not re.match(pattern_author_dict[author_item[i]], request.POST[author_item[i]]):
                result['retcode'] = 10003
                result['errkey'] = author_item[i]
                re_flag = False
                break
        if re_flag:
            try:
                author_get = Author.objects.get(author_id=request.POST['author_id'])
                author_get.name = save_html(request.POST['name'])
                author_get.age = int(request.POST['age'])
                author_get.country = save_html(request.POST['country'])
                author_get.save(update_fields=author_item[1:])
                result['retcode'] = 0
            except:
                result['retcode'] = 10001
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
    return HttpResponse(json.dumps(result), content_type='application/json')


def change_book_author(request):
    result = {
        'retcode': 10000,
        'errkey': "",
    }
    
    try:
        re_flag = True
        if not re.match(pattern_author_dict['author_id'], request.POST['author_id']):
            result['retcode'] = 10003
            result['errkey'] = "author_id"
            re_flag = False
        elif not re.match(pattern_book_dict['isbn'], request.POST['isbn']):
            result['retcode'] = 10003
            result['errkey'] = "isbn"
            re_flag = False
            
        if re_flag:
            try:
                author_get = Author.objects.get(author_id=request.POST['author_id'])
                try:
                    book_get = Book.objects.get(isbn=request.POST['isbn'])
                    book_get.author = author_get
                    book_get.save(update_fields=['author'])
                    result['retcode'] = 0
                except:
                    result['retcode'] = 10001
            except:
                result['retcode'] = 10002
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
    return HttpResponse(json.dumps(result), content_type='application/json')


def query_by_author_id_or_name(request):
    result = {
        'retcode': 10000,
        'author_count': 0,
        'book_count': 0,
        'books':[],
        'errkey': "",
    }
    
    try:
        page = int(request.POST['page'])
        re_flag = True
        if page < 0:
            result['retcode'] = 10003
            result['errkey'] = "page"
            re_flag = False
        elif request.POST['author_id'] != u"-1" and not \
            re.match(pattern_author_dict['author_id'], request.POST['author_id']):
            result['retcode'] = 10003
            result['errkey'] = "author_id"
            re_flag = False
        elif not re.match(pattern_author_dict['name'], request.POST['name']):
            result['retcode'] = 10003
            result['errkey'] = "name"
            re_flag = False
            
        if re_flag:
            author_name = request.POST['name']
            author_id = request.POST['author_id']
            if author_id != u"-1":
                author_set = Author.objects.filter(author_id=author_id, name=author_name)
            else:
                author_set = Author.objects.filter(name=author_name)
            if author_set.exists():
                result['author_count'] = author_set.count()
                for author in author_set:
                    books = author.books_for_author.all()
                    result['books'].extend(books)
                result['book_count'] = len(result['books'])
                result['books'] = [book.to_dict() for book in result['books'][(page-1)*30:page*30]]
                result['retcode'] = 0
            else:
                result['retcode'] = 10001
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
    return HttpResponse(json.dumps(result), content_type='application/json')


def query_book_by_page(request):
    result = {
        'retcode': 10000,
        'author_count': 0,
        'book_count': 0,
        'books': [],
        'errkey': "",
    }
    
    try:
        page = int(request.POST['page'])
        if page <= 0:
            result['retcode'] = 10003
            result['errkey'] = "page"
        else:
            result['author_count'] = Author.objects.all().count()
            book_set = Book.objects.all()
            result['book_count'] = book_set.count()
            result['books'] = [book.to_dict() for book in book_set[(page-1)*30:page*30]]
            result['retcode'] = 0
    except:
        print traceback.format_exc()
        result['retcode'] = 10010
    return HttpResponse(json.dumps(result), content_type='application/json')
