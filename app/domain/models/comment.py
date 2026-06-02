from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    id: Optional[int]
    post_id: int
    author: str
    content: str
    created_at: datetime