from flask import Flask, request, jsonify
from model import BookModel
from db import db_create_book, db_list_books, init_seq_id_init, seq_id_atomic_inc, db_retrieve_book, db_update_book, \
    db_delete_book
from marshmallow import INCLUDE, EXCLUDE

app = Flask(__name__)

# init db
BOOK_SEQ_NAME = 'book'
init_seq_id_init(BOOK_SEQ_NAME, 1)


@app.route("/create", methods=["POST"])
def create_book():
    """"
    Create a new book
    """
    payload = request.get_json()
    status = BookModel.Schema().validate(payload, partial=("id",))   # no validation to id
    if status:
        return jsonify(status), 400
    payload["id"] = seq_id_atomic_inc(BOOK_SEQ_NAME)
    book = BookModel(**payload)
    success = db_create_book(book)
    if not success:
        return jsonify({"message": "Book already exists"}), 409
    book_db = db_retrieve_book(book.id)
    return jsonify(data=book_db.to_dict()), 201


@app.route("/list", methods=["GET"])
def list_book():
    """"
    Retrieve all books
    """
    books = db_list_books()
    return jsonify(data=[book.to_dict() for book in books]), 200


@app.route("/retrieve", methods=["GET"])
def retrieve_book():
    """"
    Retrieve a book
    """
    book_id = request.args.get("id")
    book = db_retrieve_book(int(book_id))
    if book:
        return jsonify(data=book.to_dict()), 200
    return jsonify({"message": "Book not found"}), 404


@app.route("/update", methods=["POST"])
def update_book():
    """"
    Update a book
    """
    payload = request.get_json()
    status = BookModel.Schema().validate(payload)
    if status:
        return jsonify(status), 400
    book_id = payload.get("id")

    success = db_update_book(book_id, payload)
    if not success:
        return jsonify({"message": "Book Update failed"}), 404
    book_db = db_retrieve_book(book_id)
    return jsonify(data=book_db.to_dict()), 200


@app.route("/delete", methods=["POST"])
def delete_book():
    """"
    Delete a book
    """
    payload = request.get_json()
    book_id = payload.get("id")
    if not book_id:
        return jsonify({"message": "Book id not found"}), 400
    success = db_delete_book(book_id)
    if not success:
        return jsonify({"message": "Book Delete failed"}), 404
    return jsonify({"message": "Book Deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
