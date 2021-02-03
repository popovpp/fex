from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from django.conf.urls.static import static
from django.conf import settings

from account.views import UserViewSet
from advert.views import AdvertViewSet
from advert.views import ReplyViewSet
from advert.views import AdvertFileViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'user')
router.register(r'advert', AdvertViewSet, 'advert')
router.register(r'reply', ReplyViewSet, 'reply')
router.register(r'advertfile', AdvertFileViewSet, 'advertfile')


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
