from django.forms import ModelForm

from cms.models import Book, Impression


class BookForm(ModelForm):
    """서적 폼"""
    class Meta:
        model = Book
        fields = ('title', 'photo', 'publisher', 'page',)


class ImpressionForm(ModelForm):
    """서평 폼"""
    class Meta:
        model = Impression
        fields = ('comment',)