from django.urls import path 
from django.views.generic import RedirectView
from . import views

urlpatterns=[
    path('', RedirectView.as_view(pattern_name='register', permanent=False)),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('users/',views.user_list,name='user_list'),
    path('chat/<int:user_id>/',views.chat_view,name='chat')
]