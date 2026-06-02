from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.application.ports.out.post_repository import PostRepository
from app.domain.models.post import Post
from app.infrastructure.persistence.postgresql.post_model import PostModel

class PostPostgresAdapter(PostRepository):
    def __init__(self, db: Session):
        self.db = db

    def _to_domain(self, model: PostModel) -> Post:
        return Post(
            id=model.id,
            author=model.author,
            category=model.category,
            title=model.title,
            content=model.content,
            likes=model.likes,
            comments_count=model.comments_count,
            created_at=model.created_at
        )

    def find_all(self, page: int, size: int) -> Tuple[List[Post], int]:
        total = self.db.query(PostModel).count()
        posts = self.db.query(PostModel)\
            .order_by(PostModel.created_at.desc())\
            .offset(page * size)\
            .limit(size)\
            .all()
        return [self._to_domain(p) for p in posts], total

    def find_by_id(self, post_id: int) -> Optional[Post]:
        model = self.db.query(PostModel).filter(PostModel.id == post_id).first()
        return self._to_domain(model) if model else None

    def save(self, post: Post) -> Post:
        model = PostModel(
            author=post.author,
            category=post.category,
            title=post.title,
            content=post.content,
            likes=post.likes,
            comments_count=post.comments_count,
            created_at=post.created_at
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)

    def update(self, post: Post) -> Post:
        model = self.db.query(PostModel).filter(PostModel.id == post.id).first()
        model.likes = post.likes
        model.comments_count = post.comments_count
        self.db.commit()
        self.db.refresh(model)
        return self._to_domain(model)
