from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.models.post import Post

class PostRepository(ABC):
    @abstractmethod
    def find_all(self, page: int, size: int) -> Tuple[List[Post], int]:
        pass

    @abstractmethod
    def find_by_id(self, post_id: int) -> Optional[Post]:
        pass

    @abstractmethod
    def save(self, post: Post) -> Post:
        pass

    @abstractmethod
    def update(self, post: Post) -> Post:
        pass
