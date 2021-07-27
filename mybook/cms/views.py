from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView

from cms.forms import BookForm, ImpressionForm
from cms.models import Book, Impression

class BookList(ListView):
    """서평 목록"""

    # 데이터 키
    context_object_name = 'books'
    template_name = 'cms/book_list.html'
    paginate_by = 2

    def get(self, request):
        books = Book.objects.all().order_by('id')
        self.object_list = books

        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


# def book_list(request):
#     """Book List"""
#     # return HttpResponse('서적 목록')
#     books = Book.objects.all().order_by('id')
#     return render(request, 'cms/book_list.html', {'books': books})


def book_add(request):
    if request.method == 'GET':
        book = Book()
        form = BookForm(instance=book)
        return render(request, 'cms/book_add.html', {'form': form})
    if request.method == 'POST':
        book = Book()
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('cms:book_list')


def book_edit(request, book_id=None):
    """Book Edit"""
    if book_id:     # book_id 가 지정되어 있을 경우 -> 수정
        book = get_object_or_404(Book, pk=book_id)
    else:       # book_id가 지정되어 있지 않으면 -> 추가
        book = Book()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('cms:book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'cms/book_edit.html', dict(form=form, book_id=book_id))


def book_del(request, book_id):
    """Book Delete"""

    book = get_object_or_404(Book, pk=book_id)

    book.delete()
    return redirect('cms:book_list')


class ImpressionList(ListView):
    """서평 목록"""

    # 데이터 키
    context_object_name = 'impressions'
    template_name = 'cms/impression_list.html'
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['book_id'])
        impressions = book.impressions.all().order_by('id')
        self.object_list = impressions

        context = self.get_context_data(object_list=self.object_list, book=book)
        return self.render_to_response(context)


def impression_edit(request, book_id, impression_id=None):
    """서평 편집집"""
    book = get_object_or_404(Book, pk=book_id)
    if impression_id:
        impression = get_object_or_404(Impression, pk=impression_id)
    else:
        impression = Impression()

    if request.method == 'POST':
        form = ImpressionForm(request.POST, instance=impression)
        if form.is_valid():
            impression = form.save(commit=False)
            impression.book = book
            impression.save()
            return redirect('cms:impression_list', book_id=book_id)
    else:
        form = ImpressionForm(instance=impression)

    return render(request, 'cms/impression_edit.html', dict(form=form, book_id=book_id, impression_id=impression_id))


def impression_del(request, book_id, impression_id):
    """서평 삭제"""
    impression = get_object_or_404(Impression, pk=impression_id)
    impression.delete()
    return redirect('cms:impression_list', book_id=book_id)





