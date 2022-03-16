import pymongo
from model import *
from typing import List, Dict, Any

client = pymongo.MongoClient("mongodb://localhost:27017/")
TDb = client["data"]
TBook = TDb['book']
TCounter = TDb['seq_id']


def init_seq_id_init(name: str, v: int):
    try:
        TCounter.insert_one({"_id": name, "v": v})
    except pymongo.errors.DuplicateKeyError:
        pass


def seq_id_atomic_inc(name, inc=1) -> int:
    TCounter.update_one({"_id": name}, {"$inc": {"v": inc}})
    return TCounter.find_one({"_id": name})['v']


def db_create_book(book: BookModel) -> bool:
    try:
        TBook.insert_one(book.__dict__)
        return True
    except pymongo.errors.DuplicateKeyError:
        return False


def db_update_book(book_id: int, book: Dict[str, Any]) -> bool:
    res = TBook.update_one({"id": book_id}, {"$set": book})
    return res.modified_count > 0


def db_list_books() -> List[BookModel]:
    return [BookModel(**r) for r in TBook.find()]


def db_retrieve_book(book_id: int) -> BookModel:
    _book = TBook.find_one({"id": book_id})
    return BookModel(**_book) if _book else None


def db_delete_book(book_id: int) -> bool:
    res = TBook.delete_one({"id": book_id})
    return res.deleted_count > 0
