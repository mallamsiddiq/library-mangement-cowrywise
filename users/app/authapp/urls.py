from rest_framework.routers import DefaultRouter
from django.urls import path, include
from authapp.views import AuthViewSet
app_name = 'authapp'

router = DefaultRouter()
router.register('', AuthViewSet, basename='authentication')


urlpatterns = [
    path('auth/', include(router.urls)),
]
