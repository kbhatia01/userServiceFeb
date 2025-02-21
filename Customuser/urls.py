from django.urls import path

from Customuser import views
from Customuser.views import CustomTokenView

urlpatterns = [
    path('user_signup', views.signup, name='signup'),
    path('login', views.login,name="login"),

    path('/token', CustomTokenView.as_view(), name='token'),

    path('/sayHello', views.sayHello, name='sayHello'),
]