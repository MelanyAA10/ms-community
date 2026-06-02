from typing import List
from sqlalchemy.orm import Session
from app.application.ports.out.comment_repository import CommentRepository
from app.domain.models.comment import Comment
from app.infrastructure.persistence.postgresql.comment_model import CommentModel


class CommentPostgresAdapter(CommentRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: CommentModel) -> Comment:
        return Comment(
            id=model.id,
            post_id=model.post_id,
            author=model.author,
            content=model.content,
            created_at=model.created_at
        )

    def add(self, comment: Comment) -> Comment:
        model = CommentModel(
            post_id=comment.post_id,
            author=comment.author,
            content=comment.content,
            created_at=comment.created_at
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)

    def find_by_post(self, post_id: int) -> List[Comment]:
        models = self.db.query(CommentModel)\
            .filter(CommentModel.post_id == post_id)\
            .order_by(CommentModel.created_at.asc())\
            .all()
        return [self._to_domain(m) for m in models]