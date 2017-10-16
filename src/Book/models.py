# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Author(models.Model):
    author_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    country = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.author_id + u'_' +self.name
    
    def to_dict(self):
        return {'author_id': self.author_id,
                'name': self.name,
                'age': self.age,
                'country': self.country,}


class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, related_name='books_for_author')
    publisher = models.CharField(max_length=100)
    publish_date = models.CharField(max_length=50)
    price = models.FloatField()
    
    def __unicode__(self):
        return self.isbn + u'_' + self.title
    
    def to_dict(self):
        return {'isbn': self.isbn,
                'title': self.title,
                'author_id': self.author.author_id,
                'publisher': self.publisher,
                'publish_date': self.publish_date,
                'price': self.price,}
