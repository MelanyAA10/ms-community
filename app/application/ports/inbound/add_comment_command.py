from abc import ABC, abstractmethod
from app.domain.models.comment import Comment

class AddCommentCommand(ABC):
    @abstractmethod
    def execute(self, post_id: int, author: str, content: str) -> Comment:
        pass