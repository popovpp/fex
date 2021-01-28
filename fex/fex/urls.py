from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from account.views import UserViewSet
from advert.views import AdvertViewSet
from advert.views import ReplyViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'user')
router.register(r'advert', AdvertViewSet, 'advert')
router.register(r'reply', ReplyViewSet, 'reply')


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
