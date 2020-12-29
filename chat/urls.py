from django.urls import path, re_path


from . import views

app_name = 'chat'
urlpatterns = [
    path('home/', views.index, name="index" ),
    path('friend/<int:room_name>/', views.room, name='room'),
]
