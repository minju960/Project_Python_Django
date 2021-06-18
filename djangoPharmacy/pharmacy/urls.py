from django.urls import path

from pharmacy import views

app_name = 'pharmacy'
urlpatterns = [
    path('current_location', views.current_location, name='current_location'),
    path('geocode_find', views.geocode_find, name='geocode_find'),
    path('my_location', views.my_location, name='my_location'),
    path('query', views.query, name='query'),
]
