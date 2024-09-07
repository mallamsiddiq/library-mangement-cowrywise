from rest_framework.routers import DefaultRouter
from django.urls import path, include
from library.views import BookViewSet, IssuanceViewSet, UsersViewset
app_name = 'library'

router = DefaultRouter()
router.register('books', BookViewSet, basename='admin-on-books')
router.register('borrowing', IssuanceViewSet, basename='book-borrowing')
router.register('users', UsersViewset, basename='users')

urlpatterns = [
    path('library/', include(router.urls)),
]
