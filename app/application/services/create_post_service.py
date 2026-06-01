from datetime import datetime
from app.application.ports.in.create_post_command import CreatePostCommand
from app.application.ports.out.post_repository import PostRepository
from app.domain.models.post import Post

class CreatePostService(CreatePostCommand):
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def execute(self, author: str, category: str, title: str, content: str) -> Post:
        post = Post(
            id=None,
            author=author,
            category=category,
            title=title,
            content=content,
            likes=0,
            comments_count=0,
            created_at=datetime.utcnow()
        )
        return self.post_repository.save(post)
