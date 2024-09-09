
from utils.models import CustomEnum

class CategoryChoices(CustomEnum):
    FICTION = "Fiction"
    TECHNOLOGY = "Technology"
    SCIENCE = "Science"


class PublisherChoices(CustomEnum):
    WILEY = "Wiley"
    APRESS = "Apress"
    MANNING = "Manning"

