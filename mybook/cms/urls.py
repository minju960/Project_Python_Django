"""mybook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from cms import views



app_name = 'cms'
urlpatterns = [
    # path('book/', views.book_list, name='book_list'),
    path('book/', views.BookList.as_view(), name='book_list'),
    path('book/add', views.book_edit, name='book_add'),
    path('book/mod/<int:book_id>', views.book_edit, name='book_mod'),
    path('book/del/<int:book_id>', views.book_del, name='book_del'),
    path('book/book_add', views.book_add, name='book_add_process'),

    path('impression/<int:book_id>', views.ImpressionList.as_view(), name='impression_list'),
    path('impression/add/<int:book_id>', views.impression_edit, name='impression_add'),
    path('impression/mod/<int:book_id>/<int:impression_id>', views.impression_edit, name='impression_mod'),
    path('impression/del/<int:book_id>/<int:impression_id>', views.impression_del, name='impression_del'),
]
