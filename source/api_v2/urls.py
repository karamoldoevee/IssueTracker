from django.urls import include, path

from rest_framework import routers

from api_v2 import views

router = routers.DefaultRouter()

router.register(r'issues', views.IssueViewSet)

app_name = 'api_v2'

urlpatterns = [

    path('', include(router.urls)),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]