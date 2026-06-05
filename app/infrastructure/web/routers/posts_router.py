import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.persistence.postgresql.database import get_db
from app.infrastructure.persistence.repositories.post_postgres_adapter import PostPostgresAdapter
from app.infrastructure.persistence.repositories.comment_postgres_adapter import CommentPostgresAdapter
from app.application.services.get_posts_service import GetPostsService
from app.application.services.create_post_service import CreatePostService
from app.application.services.like_post_service import LikePostService
from app.application.services.add_comment_service import AddCommentService
from app.application.services.get_comments_service import GetCommentsService
from app.infrastructure.web.dto.post_dto import (
    CreatePostDto,
    PostResponseDto,
    PagedResponseDto,
    CreateCommentDto,
    CommentResponseDto,
)
from app.domain.exceptions.post_not_found import PostNotFoundException

router = APIRouter()

def get_post_repository(db: Session = Depends(get_db)):
    return PostPostgresAdapter(db)

def get_comment_repository(db: Session = Depends(get_db)):
    return CommentPostgresAdapter(db)

# --- Crear post ---
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

# --- Like ---
@router.post("/posts/{post_id}/like", response_model=PostResponseDto)
def like_post(post_id: int, action: str = "like", repo=Depends(get_post_repository)):
    service = LikePostService(repo)
    try:
        post = service.execute(post_id, action)
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

# --- Comentarios (ANTES de /posts/{page}/{size} para evitar el choque de rutas) ---
@router.post("/posts/{post_id}/comments", response_model=CommentResponseDto, status_code=201)
def add_comment(post_id: int, body: CreateCommentDto,
                comment_repo=Depends(get_comment_repository),
                post_repo=Depends(get_post_repository)):
    service = AddCommentService(comment_repo, post_repo)
    try:
        comment = service.execute(post_id, body.author, body.content)
        return CommentResponseDto(
            id=comment.id,
            post_id=comment.post_id,
            author=comment.author,
            content=comment.content,
            created_at=comment.created_at
        )
    except PostNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/posts/{post_id}/comments", response_model=list[CommentResponseDto])
def get_comments(post_id: int, comment_repo=Depends(get_comment_repository)):
    service = GetCommentsService(comment_repo)
    comments = service.execute(post_id)
    return [
        CommentResponseDto(
            id=c.id,
            post_id=c.post_id,
            author=c.author,
            content=c.content,
            created_at=c.created_at
        ) for c in comments
    ]

# --- Listar posts paginado (ruta generica: va de ULTIMA) ---
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