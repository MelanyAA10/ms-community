from app.application.ports.out.post_repository import PostRepository
from app.domain.exceptions.post_not_found import PostNotFoundException

class DeletePostService:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    def execute(self, post_id: int) -> None:
        post = self.repo.find_by_id(post_id)
        if not post:
            raise PostNotFoundException(f"Post with id {post_id} not found")
        self.repo.delete(post_id)