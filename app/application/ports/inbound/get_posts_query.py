from abc import ABC, abstractmethod
from typing import List, Tuple
from app.domain.models.post import Post

class GetPostsQuery(ABC):
    @abstractmethod
    def execute(self, page: int, size: int) -> Tuple[List[Post], int]:
        pass
