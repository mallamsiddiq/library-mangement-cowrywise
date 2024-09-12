from rest_framework.routers import DefaultRouter
from django.urls import path, include
from library.views import BookViewSet
app_name = 'library'

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')


urlpatterns = [
    path('library/', include(router.urls)),
]
