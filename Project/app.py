from flask import Flask, url_for, redirect, session, request, render_template  # import các module cần thiết
from db_config import mydb, cursor # kết nối và tương tác với cơ sở dữ liệu
from PIL import Image   #  xử lý hình ảnh
import io   #
import base64

# Khởi tạo một đối tượng ứng dụng Flask
app = Flask(__name__)
# Đặt giá trị secret key đê bảo vệ session
app.secret_key = "Dungdz1st"


#Trang Home
@app.route('/')
def home():
   cursor.execute("SELECT * FROM books")  # truy vấn dữ liệu từ bảng books
   books = cursor.fetchall() # gắn kết quả truy vấn vào books
   role = session.get('role') # Lấy role từ session
   return render_template('index.html', books = books, len = len(books), base64 = base64, get_user_fullname = get_user_fullname, role = role)


# Thao tác của người dùng
# Trang đăng ký tài khoản
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # Lấy các giá trị trong trường từ biểu mẫu gán vào biến tương ứng
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        # Kiểm tra sdt đã tồn tại hay chưa 
        cursor.execute('SELECT phone_number FROM users WHERE phone_number = %s', (phone_number,))
        exit_user = cursor.fetchone()
        if exit_user:
            return "Số điện thoại đã đăng ký <a href=\"/register\">Quay lại</a>"
        else:
            sql = f'INSERT INTO users (phone_number, email, full_name, password, role)  VALUES ("{phone_number}", "{email}", "{full_name}", "{password}", "member"  )'
            cursor.execute(sql)
            mydb.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

# Trang đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lấy giá trị trong biểu mẫu login gán vào các biên tương ứng
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        sql = 'SELECT * FROM users WHERE phone_number = %s AND password = %s'
        cursor.execute(sql, (phone_number, password))
        # Lấy kết quả truy vấn đầu tiên từ cursor gán vào biến user
        user = cursor.fetchone()
        # Kiểm tra user có chưa
        if user:
            role = user[4]
            session['role'] = role
            session['phone_number'] = user[0]
            return redirect(url_for('home'))
        else:
            return "Sai mật khẩu hoặc tài khoản <a href=\"/login\">Quay lại</a>"
    return render_template('login.html')
 
 
# Đường dẫn đăng xuất 
@app.route('/logout')
def logout():
   # Xóa các giá trị trả về Noe
   session.pop('role', None)
   session.pop('phone_number', None)
   return redirect(url_for('login'))


def get_user_fullname(phone_number):
   # Lầy full_name từ bảng users với số điện thoại tương ứng
   cursor.execute('SELECT full_name FROM users WHERE phone_number = %s', (phone_number,))
   result = cursor.fetchone()
   if result:
      return result[0]
   else:
      return 'Người dùng'


# Trang thao tác với sách
@app.route('/crud')
def crud():
   # Lấy giá trị từ khóa role gán vào bién role và kiểm tra nếu không phải admin trả về home
   role = session.get('role')
   if role != 'admin':
      return redirect(url_for('home'))
   
   # Tạo chức năng tìm kiếm
   title = request.args.get('title')
   # Thực hiện chức năng truy vấn csdl lấy tất cả các trường từ bảng books với tiêu đề title lấy từ biểu mẩu trên
   if title != None:
      cursor.execute(f'SELECT * FROM books WHERE Title LIKE "%{title}%"')
   else:
      # Trả về bảng books như ban đầu
      cursor.execute('SELECT * FROM books')
   # Lấy tất cả truy vấn từ cursor và gán cho biến books
   books = cursor.fetchall()
   return render_template('crud.html', books=books, len=len(books), base64=base64)

# Tạo đường dẫn add book
@app.route('/add', methods = ['POST'])
def add():
   # Kiểm tra xem phương thức có phải là Post hay không
   if request.method == 'POST':
      book_id = request.form.get('book_id')
      title = request.form.get('title')
      author = request.form.get('author')
      genre = request.form.get('genre')
      year = request.form.get('year')
      price = request.form.get('price')
      img = request.files.get('img')
      # Xử lý hình ảnh
      img_binary = None
      if img:
         img_file = request.files['img']
         img_data = img_file.read()
         img_pil = Image.open(io.BytesIO(img_data))
         img_buffer = io.BytesIO()
         img_pil.save(img_buffer, format='JPEG')
         img_binary = img_buffer.getvalue()
         img_base64 = base64.b64encode(img_data)

      # Kiểm tra tác giả đã tồn tại trong bảng hay chưa
      sql_check_author = f"SELECT * FROM authors WHERE AuthorName = '{author}'"
      cursor.execute(sql_check_author)
      author_result = cursor.fetchone()

      if not author_result:
          # Thêm tác giả mới nếu không tồn tại trong bảng
          sql_add_author = f"INSERT IGNORE INTO authors (AuthorName) VALUES ('{author}')"
          cursor.execute(sql_add_author)
          mydb.commit()

      # Kiểm tra thể loại đã tồn tại trong bảng hay chưa
      sql_check_genre = f"SELECT * FROM genres WHERE GenreName = '{genre}'"
      cursor.execute(sql_check_genre)
      genre_result = cursor.fetchone()

      if not genre_result:
          # Thêm thể loại mới nếu không tồn tại trong bảng
          sql_add_genre = f"INSERT IGNORE INTO genres (GenreName) VALUES ('{genre}')"
          cursor.execute(sql_add_genre)
          mydb.commit()

      # Thêm thông tin book vào cơ sở dữ liệu
      sql = f'INSERT INTO books (BookID, Title, AuthorName, GenreName, PublishYear, Price, Image) VALUES (%s, %s, %s, %s, %s, %s, %s)'
      val = (book_id, title, author, genre, year, price, img_binary)
      cursor.execute(sql, val)
      mydb.commit()

   # Trả về đường dẫn crud
   return redirect('/crud')


@app.route('/update', methods=['GET', 'POST'] )
def update():
   if request.method == 'POST':
      book_id = request.form.get('book_id')
      title = request.form.get('title')
      author = request.form.get('author')
      genre = request.form.get('genre')
      year = request.form.get('year')
      price = request.form.get('price')
      img = request.files.get('img')
      # Xử lý hình ảnh
      img_binary = None
      if img:
         img_file = request.files['img']
         img_data = img_file.read()
         img_pil = Image.open(io.BytesIO(img_data))
         img_buffer = io.BytesIO()
         img_pil.save(img_buffer, format='JPEG')
         img_binary = img_buffer.getvalue()
         img_base64 = base64.b64encode(img_data)
         
      # Kiểm tra tác giả và thể loại đã tồn tại trong bảng hay chưa
      sql_check_author = f"SELECT * FROM authors WHERE AuthorName = '{author}'"
      cursor.execute(sql_check_author)
      author_result = cursor.fetchone()

      if not author_result:
          # Thêm tác giả mới nếu không tồn tại trong bảng
          sql_add_author = f"INSERT IGNORE INTO authors (AuthorName) VALUES ('{author}')"
          cursor.execute(sql_add_author)
          mydb.commit()

      sql_check_genre = f"SELECT * FROM genres WHERE GenreName = '{genre}'"
      cursor.execute(sql_check_genre)
      genre_result = cursor.fetchone()

      if not genre_result:
          # Thêm thể loại mới nếu không tồn tại trong bảng
          sql_add_genre = f"INSERT IGNORE INTO genres (GenreName) VALUES ('{genre}')"
          cursor.execute(sql_add_genre)
          mydb.commit()

       # Thêm thông tin book vào cơ sở dữ liệu
      sql = 'UPDATE books SET title = %s, AuthorName = %s, GenreName = %s, PublishYear = %s, Price = %s, Image = %s WHERE BookID = %s'
      val = (title, author, genre, year, price, img_binary, book_id)
      cursor.execute(sql, val)
      mydb.commit()
      # trả về đường dẫn crud
   return redirect('/crud')


@app.route('/delete/<book_id>')
def delete(book_id):
   sql = f'DELETE FROM books WHERE BookID = {book_id}'
   cursor.execute(sql)
   mydb.commit()
   return redirect('/crud')


@app.route('/author')
def author():
   role = session.get('role')
   if role != 'admin':
      return redirect(url_for('home'))
   
   name = request.args.get('name')
   if name != None:
      cursor.execute(
         f'SELECT * FROM authors WHERE AuthorName LIKE "%{name}%"')
   else:
      cursor.execute('SELECT * FROM authors')
   authors = cursor.fetchall()
   return render_template('author.html', authors = authors, len = len(authors))
   

@app.route('/add_author', methods= ['POST'])
def addAuthor():   
   if request.method == 'POST':
      authorname = request.form.get('authorname')
      nationality = request.form.get('nationality')
      birthdate = request.form.get('birthdate')
      sql = f'INSERT INTO authors (AuthorName, Nationality, BirthDate) VALUES (%s, %s, %s)'
      val = (authorname, nationality, birthdate)
      cursor.execute(sql, val)
      mydb.commit()
   return redirect('/author')


@app.route('/update_author', methods= ['GET', 'POST'])
def updateAuthor():
   if request.method == 'POST':
      authorname = request.form.get('authorname')
      nationality = request.form.get('nationality')
      birthdate = request.form.get('birthdate')
      sql = 'UPDATE authors SET Nationality = %s, BirthDate = %s WHERE AuthorName = %s'
      val = (nationality, birthdate, authorname)
      cursor.execute(sql, val)
      mydb.commit()
   return redirect('/author')


@app.route('/delete_author/<authorname>')
def deleteAuthor(authorname):
   sql = f"SELECT COUNT(*) FROM books WHERE AuthorName = '{authorname}'"
   cursor.execute(sql)
   count = cursor.fetchone()[0]
   if count > 0:
      return "Không thể xóa tác giả này vì còn sách thuộc về tác giả."
   else:
      sql = f"DELETE FROM authors WHERE AuthorName = '{authorname}'"
      cursor.execute(sql)
      mydb.commit()
      return redirect('/author')
   
   
# Trang CRUD thể loại   
@app.route('/genre')
def genre():
   role = session.get('role')
   if role != 'admin':
      return redirect(url_for('home'))
   
   genre = request.args.get('genre')
   if genre != None:
      cursor.execute(
         f'SELECT * FROM genres WHERE GenreName LIKE "%{genre}"')
   else:
      cursor.execute('SELECT * FROM genres')
   genres = cursor.fetchall()
   return render_template('genre.html', genres = genres, len = len(genres))


@app.route('/add_genre', methods = ['POST'])
def addGenre():
   role = session.get('role')
   if role != 'admin':
      return redirect(url_for('home'))
   
   if request.method == 'POST':
      genrename = request.form.get('genrename')
      description = request.form.get('description')
      sql = f'INSERT INTO genres (GenreName, Description) VALUES (%s, %s)'
      val = (genrename, description)
      cursor.execute(sql, val)
      mydb.commit()
   return redirect('/genre')
   
   
@app.route('/update_genre', methods = ['GET', 'POST'])
def updateGenre():
   role = session.get('role')
   if role != 'admin':
      return redirect(url_for('home'))
   
   if request.method == 'POST':
      genrename = request.form.get('genrename')     
      description = request.form.get('description')
      sql = 'UPDATE genres SET Description = %s WHERE GenreName = %s'
      val = (description, genrename)
      cursor.execute(sql, val)
      mydb.commit()
   return redirect('/genre')


@app.route('/delete_genre/<genrename>')
def deleteGenre(genrename):
   sql = f"SELECT COUNT(*) FROM books WHERE GenreName = '{genrename}'"
   cursor.execute(sql)
   count = cursor.fetchone()[0]
   if count > 0:
      return "Không thể xóa thể loại này vì còn sách thuộc thể loại này."
   else:
      sql = f"DELETE FROM genres WHERE GenreName = '{genrename}'"
      cursor.execute(sql)
      mydb.commit()
      return redirect('/genre')
   
   
# user

@app.route('/user')
def user():
   role = session.get('role')
   if role != 'admin':
      return redirect(url_for('home'))
   
   name = request.args.get('name')
   if name != None:
      cursor.execute(
         f'SELECT * FROM users WHERE userName LIKE "%{name}%"')
   else:
      cursor.execute('SELECT * FROM users')
   users = cursor.fetchall()
   return render_template('user.html', users = users, len = len(users))


   
if __name__ == '__main__':
    app.run(debug=True)