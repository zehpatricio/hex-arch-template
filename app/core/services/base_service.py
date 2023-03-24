from app.persistence.repository import BaseRepository


class BaseService:
    """
    Base class for services.

    Attributes:
        repository (persistence.BaseRepository): The repository instance used
            by the service.

    Methods:
        init(self, repository: persistence.BaseRepository): Initializes the
            service with a repository instance.
    """
    repository: BaseRepository

    def __init__(self, repository: BaseRepository) -> None:
        self.repository = repository
