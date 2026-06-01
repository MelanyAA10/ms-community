from app.application.ports.inbound.like_post_command import LikePostCommand
from app.application.ports.out.post_repository import PostRepository
from app.domain.models.post import Post
from app.domain.exceptions.post_not_found import PostNotFoundException

class LikePostService(LikePostCommand):
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def execute(self, post_id: int) -> Post:
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise PostNotFoundException(post_id)
        post.likes += 1
        return self.post_repository.update(post)