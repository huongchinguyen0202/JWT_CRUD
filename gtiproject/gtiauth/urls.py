from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from gtiauth import views

urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^login/', views.GtiAuth.api_login, name="api_login"),
]
