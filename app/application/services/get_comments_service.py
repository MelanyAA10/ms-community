from typing import List
from app.application.ports.inbound.get_comments_query import GetCommentsQuery
from app.application.ports.out.comment_repository import CommentRepository
from app.domain.models.comment import Comment


class GetCommentsService(GetCommentsQuery):
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def execute(self, post_id: int) -> List[Comment]:
        return self.comment_repository.find_by_post(post_id)