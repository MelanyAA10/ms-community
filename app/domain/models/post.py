from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Post:
    id: Optional[int]
    author: str
    category: str  # Reviews, Recommendations, Community
    title: str
    content: str
    likes: int
    comments_count: int
    created_at: datetime
