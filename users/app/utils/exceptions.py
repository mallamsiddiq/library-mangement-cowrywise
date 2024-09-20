from rest_framework.exceptions import APIException


class BookNotAvailableException(APIException):
    status_code = 400
    default_detail = 'The requested book is not available for borrowing.'
    default_code = 'book_not_available'
    
    
class UserNotFoundException(APIException):
    status_code = 404
    default_detail = 'Provide Your Id or pass in Authentication Token'
    default_code = 'user_not_found'