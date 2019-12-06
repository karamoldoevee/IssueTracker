from django.urls import include, path

from rest_framework import routers

from api_v2 import views

from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()

router.register(r'issues', views.IssueViewSet)

router.register(r'projects', views.ProjectViewSet)

app_name = 'api_v2'

urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth')
]