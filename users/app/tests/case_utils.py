# test_mixins.py
from unittest.mock import patch
from django.conf import settings


class IgnoreEventBusActionsMixin:
    
    patch_targets = ['events.producers.send_users_updates.publish_to_network', 
                      'events.producers.send_book_updates.publish_to_network', 
                      'events.producers.send_borrow_updates.publish_to_network']
    
    __mock_patchers = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.patch_targets:
            raise ValueError("patch_target must be set in the subclass")
        
        for patch_target in cls.patch_targets:
            patcher = patch(patch_target)
            patcher.start()
            cls.__mock_patchers.append(patcher)
            

    @classmethod
    def tearDownClass(cls):
        for patcher in cls.__mock_patchers:
            patcher.stop()
        super().tearDownClass()
        
        
def mock_auth_service_call(auth_url=settings.AUTH_SERVICE_URL, 
                                token='testtoken123'):
    """
    Custom decorator to mock authentication service.
    """
    def decorator(func):
        @patch('utils.middleware.requests.get')  # Mock the requests.get method used in your custom JWT middleware
        def wrapper(self, mock_get, *args, **kwargs):
            # Mock the authentication response
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = {
                'id': str(self.user.pk),
                'email': self.user.email,
                'is_staff': self.user.is_staff,
                'is_active': self.user.is_active,
            }

            # Call the original test function
            return func(self, *args, **kwargs)
        return wrapper
    return decorator