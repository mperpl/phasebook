from datetime import datetime

from pydantic import BaseModel, ConfigDict
from schemas.comment import CommentRead


class WritePost(BaseModel):
    content: str


class ReadPost(BaseModel):
    author_id: int
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostDiscussionRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    # This is the magic line that nests the comments
    comments: list[CommentRead] = []

    model_config = ConfigDict(from_attributes=True)