import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.persistence.postgresql.database import get_db
from app.infrastructure.persistence.repositories.post_postgres_adapter import PostPostgresAdapter
from app.application.services.get_posts_service import GetPostsService
from app.application.services.create_post_service import CreatePostService
from app.application.services.like_post_service import LikePostService
from app.infrastructure.web.dto.post_dto import CreatePostDto, PostResponseDto, PagedResponseDto
from app.domain.exceptions.post_not_found import PostNotFoundException

router = APIRouter()

def get_post_repository(db: Session = Depends(get_db)):
    return PostPostgresAdapter(db)

@router.get("/posts/{page}/{size}", response_model=PagedResponseDto)
def get_posts(page: int, size: int, repo=Depends(get_post_repository)):
    service = GetPostsService(repo)
    posts, total = service.execute(page, size)
    total_pages = math.ceil(total / size) if size > 0 else 0
    return PagedResponseDto(
        content=[PostResponseDto(
            id=p.id,
            author=p.author,
            category=p.category,
            title=p.title,
            content=p.content,
            likes=p.likes,
            comments_count=p.comments_count,
            created_at=p.created_at
        ) for p in posts],
        page=page,
        size=size,
        total_elements=total,
        total_pages=total_pages
    )

@router.post("/posts", response_model=PostResponseDto, status_code=201)
def create_post(body: CreatePostDto, repo=Depends(get_post_repository)):
    service = CreatePostService(repo)
    post = service.execute(body.author, body.category, body.title, body.content)
    return PostResponseDto(
        id=post.id,
        author=post.author,
        category=post.category,
        title=post.title,
        content=post.content,
        likes=post.likes,
        comments_count=post.comments_count,
        created_at=post.created_at
    )

@router.post("/posts/{post_id}/like", response_model=PostResponseDto)
def like_post(post_id: int, repo=Depends(get_post_repository)):
    service = LikePostService(repo)
    try:
        post = service.execute(post_id)
        return PostResponseDto(
            id=post.id,
            author=post.author,
            category=post.category,
            title=post.title,
            content=post.content,
            likes=post.likes,
            comments_count=post.comments_count,
            created_at=post.created_at
        )
    except PostNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
