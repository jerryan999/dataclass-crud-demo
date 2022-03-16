from dataclasses import field
from datetime import datetime

from marshmallow_dataclass import dataclass as mm_dataclass
from typing import Optional, List
from dataclasses_json import dataclass_json, Undefined
from marshmallow import validate
from enum import Enum


class BookGenreType(Enum):
    FICTION = 1
    NON_FICTION = 2
    ROMANCE = 3
    MYSTERY = 4
    HORROR = 5
    SCIFI = 6


BookGenreValueList = [e.value for e in BookGenreType]


@dataclass_json(undefined=Undefined.EXCLUDE)
@mm_dataclass(frozen=True)
class BookModel:
    """{
            "id": 1,
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "year": 1925,
            "genre": "Fiction",
            "description": "The Great Gatsby is a 1925 novel written by American author ...",
            "image": "https://images-na.ssl-images-amazon.com/images/I/51ZrKb%2BQmL.jpg",
            "rating": 4.5
        }"""
    id: int  # no validation
    author: Optional[str]
    title: str = field(metadata={"validate": validate.Length(min=1, max=256)})
    year: Optional[int]
    genre: Optional[int] = field(metadata={
        "validate": validate.OneOf(BookGenreValueList)
    })
    description: Optional[str]
    image: Optional[str]
    rating: Optional[float]
    created_at: datetime = field(metadata={
        'dataclasses_json': {
            'encoder': lambda x: datetime.timestamp(x),
        }
    }, default_factory=datetime.utcnow)
