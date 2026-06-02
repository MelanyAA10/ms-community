from pydantic import BaseModel
from datetime import datetime
from typing import List, Generic, TypeVar

T = TypeVar("T")

class CreatePostDto(BaseModel):
    author: str
    category: str
    title: str
    content: str

class PostResponseDto(BaseModel):
    id: int
    author: str
    category: str
    title: str
    content: str
    likes: int
    comments_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class PagedResponseDto(BaseModel):
    content: List[PostResponseDto]
    page: int
    size: int
    total_elements: int
    total_pages: int

#nuevos
class CreateCommentDto(BaseModel):
    author: str
    content: str

class CommentResponseDto(BaseModel):
    id: int
    post_id: int
    author: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True