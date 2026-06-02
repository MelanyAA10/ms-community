from abc import ABC, abstractmethod
from typing import List
from app.domain.models.comment import Comment

class CommentRepository(ABC):
    @abstractmethod
    def add(self, comment: Comment) -> Comment:
        pass

    @abstractmethod
    def find_by_post(self, post_id: int) -> List[Comment]:
        pass