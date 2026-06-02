from datetime import datetime
from app.application.ports.inbound.add_comment_command import AddCommentCommand
from app.application.ports.out.comment_repository import CommentRepository
from app.application.ports.out.post_repository import PostRepository
from app.domain.models.comment import Comment
from app.domain.exceptions.post_not_found import PostNotFoundException


class AddCommentService(AddCommentCommand):
    def __init__(self, comment_repository: CommentRepository, post_repository: PostRepository):
        self.comment_repository = comment_repository
        self.post_repository = post_repository

    def execute(self, post_id: int, author: str, content: str) -> Comment:
        post = self.post_repository.find_by_id(post_id)
        if not post:
            raise PostNotFoundException(post_id)

        comment = Comment(
            id=None,
            post_id=post_id,
            author=author,
            content=content,
            created_at=datetime.utcnow()
        )
        saved = self.comment_repository.add(comment)

        post.comments_count += 1
        self.post_repository.update(post)

        return saved