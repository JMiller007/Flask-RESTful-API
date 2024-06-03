from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

books = {}

def abort_if_book_doesnt_exist(book_id):
    if book_id not in books:
        abort(404, message="Book {} doesn't exist".format(book_id))

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help='Title of the book is required')
parser.add_argument('author', type=str, required=True, help='Author of the book is required')
parser.add_argument('published', type=str, required=True, help='Publication date of the book is required')

class Book(Resource):
    def get(self, book_id):
        abort_if_book_doesnt_exist(book_id)
        return books[book_id]

    def delete(self, book_id):
        abort_if_book_doesnt_exist(book_id)
        del books[book_id]
        return '', 204

    def put(self, book_id):
        args = parser.parse_args()
        book = {'title': args['title'], 'author': args['author'], 'published': args['published']}
        books[book_id] = book
        return book, 201

class BookList(Resource):
    def get(self):
        return books

    def post(self):
        args = parser.parse_args()
        book_id = int(max(books.keys() or [0])) + 1
        book_id = str(book_id)
        books[book_id] = {'title': args['title'], 'author': args['author'], 'published': args['published']}
        return books[book_id], 201

@app.route('/')
def home():
    return render_template('index.html')

api.add_resource(BookList, '/api/books')
api.add_resource(Book, '/api/books/<book_id>')

if __name__ == '__main__':
    app.run(debug=True)
