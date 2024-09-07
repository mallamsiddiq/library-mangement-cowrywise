from rest_framework.routers import DefaultRouter
from django.urls import path, include
from users.views import BookViewSet
app_name = 'users'

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')


urlpatterns = [
    path('users/', include(router.urls)),
]
