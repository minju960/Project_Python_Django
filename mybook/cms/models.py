from django.db import models


class Book(models.Model):
    """서적"""
    title = models.CharField(verbose_name='서적명', max_length=255)
    photo = models.ImageField(upload_to='images/', blank=True)
    publisher = models.CharField(verbose_name='출판사', max_length=255, blank=True)
    page = models.IntegerField(verbose_name='페이지 수', blank=True, default=0)

    def __str__(self):
        return f'서적명 : {self.title} / 사진 : {self.photo} / 출판사 : {self.publisher} / 페이지 수 : {self.page}'

    class Meta:
        db_table = 'book'


class Impression(models.Model):
    """서평"""
    book = models.ForeignKey(Book, verbose_name='서적', related_name='impressions', on_delete=models.CASCADE)
    comment = models.TextField(verbose_name='서평', blank=True)

    def __str__(self):
        return f'서평 : {self.comment}'

    class Meta:
        db_table = 'impression'
