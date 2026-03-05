from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class WriteComment(BaseModel):
    content: str = Field(min_length=1, max_length=1000)


class CommentRead(BaseModel):
    id: int
    content: str
    author_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)