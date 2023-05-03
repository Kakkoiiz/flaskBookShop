from flask import Flask, url_for, redirect, session, request, render_template
from db_config import mydb, cursor
from PIL import Image
import io
import base64

app = Flask(__name__)
app.secret_key = "Dungdz1st"

@app.route('/')
def home():
   cursor.execute("SELECT * FROM books")
   books = cursor.fetchall()
   return render_template('index.html', books = books, len = len(books), base64 = base64)

@app.route('/crud')
def crud():
   title = request.args.get('title')
   
   if title != None:
      cursor.execute(
         f'SELECT * FROM books WHERE title LIKE "%{title}%"')
   else:
      cursor.execute('SELECT * FROM books')
   books = cursor.fetchall()
   return render_template('crud.html', books = books, len = len(books), base64 = base64)


if __name__ == '__main__':
    app.run(debug=True)