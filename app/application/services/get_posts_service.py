from typing import List, Tuple
from app.application.ports.in.get_posts_query import GetPostsQuery
from app.application.ports.out.post_repository import PostRepository
from app.domain.models.post import Post

class GetPostsService(GetPostsQuery):
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def execute(self, page: int, size: int) -> Tuple[List[Post], int]:
        return self.post_repository.find_all(page, size)
