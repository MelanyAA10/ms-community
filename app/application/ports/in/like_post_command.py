from abc import ABC, abstractmethod
from app.domain.models.post import Post

class LikePostCommand(ABC):
    @abstractmethod
    def execute(self, post_id: int) -> Post:
        pass
