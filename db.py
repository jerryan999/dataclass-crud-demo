import pymongo
from model import *
from typing import List, Dict, Any

client = pymongo.MongoClient("mongodb://localhost:27017/")
TDb = client["data"]
TBook = TDb['book']


def db_create_book(book: BookModel) -> bool:
    TBook.insert_one(book.__dict__)


def db_update_book(book_id: str, book: Dict[str, Any]) -> bool:
    res = TBook.update_one({"id": book_id}, {"$set": book})
    return res.modified_count > 0


def db_list_books() -> List[BookModel]:
    return [BookModel.from_dict(r) for r in TBook.find()]


def db_retrieve_book(book_id: str) -> BookModel:
    _book = TBook.find_one({"id": book_id})
    return BookModel.from_dict(_book) if _book else None


def db_delete_book(book_id: str) -> bool:
    res = TBook.delete_one({"id": book_id})
    return res.deleted_count > 0
