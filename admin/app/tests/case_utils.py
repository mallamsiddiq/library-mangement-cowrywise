# test_mixins.py
from unittest.mock import patch


class IgnoreEventBusActionsMixin:
    
    patch_targets = ['events.producers.send_users_updates.publish_to_network', 
                      'events.producers.send_book_updates.publish_to_network',]
    
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
