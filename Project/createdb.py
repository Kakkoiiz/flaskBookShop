import mysql.connector

# Kết nối đến cơ sở dữ liệu MySQL
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456'
)

# Tạo cơ sở dữ liệu 'qls'
cursor = mydb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS ql")
cursor.execute("USE qls")
# Tạo bảng Authors
cursor.execute("CREATE TABLE IF NOT EXISTS Authors (AuthorName VARCHAR(255) PRIMARY KEY, Nationality VARCHAR(255), BirthDate DATE)")

# Tạo bảng Genres
cursor.execute("CREATE TABLE IF NOT EXISTS Genres (GenreName VARCHAR(255) PRIMARY KEY, Description TEXT)")

# Tạo bảng Books
cursor.execute("CREATE TABLE IF NOT EXISTS Books (BookID INT PRIMARY KEY, Title VARCHAR(255), AuthorName VARCHAR(255), GenreName VARCHAR(255), PublishYear INT, Price DECIMAL(10,2),Image LONGBLOB ,FOREIGN KEY (AuthorName) REFERENCES Authors(AuthorName), FOREIGN KEY (GenreName) REFERENCES Genres(GenreName))")

# Tạo bảng User
cursor.execute("CREATE TABLE IF NOT EXISTS users (phone_number VARCHAR(20) PRIMARY KEY, email VARCHAR(50), full_name VARCHAR(50), password VARCHAR(255), role VARCHAR(20))")

# Thêm một bản ghi vào bảng User
cursor.execute(f'INSERT INTO users (phone_number, email, full_name, password, role) VALUES ("123456", "admin@gmail.com", "admin", "12345", "admin")')
mydb.commit()
# Đóng kết nối MySQL
mydb.close()