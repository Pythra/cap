from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('announcement/', views.announcement_form, name='announcement_form'),
    path('profile/update/', views.profile_form, name='profile_edit'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_form'),
    path('post/<slug:slug>/update/', views.PostUpdate.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDelete.as_view(), name='post_confirm_delete'),
    path('capital/trade/', views.trade, name='trade'),
    path('user/settings/', views.settings, name='settings'),
    ]
