import uuid
from dataclasses import field
from datetime import datetime

from marshmallow_dataclass import dataclass as mm_dataclass
from typing import Optional, List
from dataclasses_json import dataclass_json, Undefined
from marshmallow import validate


@dataclass_json(undefined=Undefined.EXCLUDE)
@mm_dataclass(frozen=True)
class BookModel:
    author: Optional[str]
    title: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    year: Optional[int]
    genre: Optional[int]
    description: Optional[str]
    image: Optional[str]
    rating: Optional[float]

    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: datetime = field(metadata={
        'dataclasses_json': {
            'encoder': lambda x: datetime.timestamp(x),
        }
    }, default_factory=datetime.utcnow)
