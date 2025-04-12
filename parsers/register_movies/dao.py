from config.base import BaseDAO
from .models import RegisterMovie


class RegisterMovieDAO(BaseDAO):
    """
    DAO class for managing RegisterMovie model operations. Inherits methods from BaseDAO
    """
    model = RegisterMovie
