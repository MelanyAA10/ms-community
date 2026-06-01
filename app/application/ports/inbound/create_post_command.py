from abc import ABC, abstractmethod
from app.domain.models.post import Post

class CreatePostCommand(ABC):
    @abstractmethod
    def execute(self, author: str, category: str, title: str, content: str) -> Post:
        pass
