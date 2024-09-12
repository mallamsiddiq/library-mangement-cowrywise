from rest_framework.exceptions import APIException


class BookNotAvailableException(APIException):
    status_code = 400
    default_detail = 'The requested book is not available for borrowing.'
    default_code = 'book_not_available'