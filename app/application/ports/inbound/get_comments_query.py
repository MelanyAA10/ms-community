from abc import ABC, abstractmethod
from typing import List
from app.domain.models.comment import Comment

class GetCommentsQuery(ABC):
    @abstractmethod
    def execute(self, post_id: int) -> List[Comment]:
        pass