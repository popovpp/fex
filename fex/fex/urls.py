from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from account import views
#from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('users/', views.UserList.as_view()),
    #path('users/<int:pk>/', views.UserDetail.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]


#urlpatterns = format_suffix_patterns(urlpatterns)
