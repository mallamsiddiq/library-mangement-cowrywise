from rest_framework.routers import DefaultRouter
from django.urls import path, include
from library.views import BookViewSet, IssuanceViewSet, LibraryUsersViewset
app_name = 'library'

router = DefaultRouter()
router.register('books', BookViewSet, basename='books')
router.register('borrowing', IssuanceViewSet, basename='book-borrowing')
router.register('users', LibraryUsersViewset, basename='users')

urlpatterns = [
    path('library/', include(router.urls)),
]
