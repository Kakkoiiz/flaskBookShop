import mysql.connector

# Kết nối đến cơ sở dữ liệu MySQL
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456'
)

# Tạo cơ sở dữ liệu 'qls'
cursor = mydb.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS qlsach")
cursor.execute("USE qlsach")
# Tạo bảng Authors
cursor.execute("CREATE TABLE IF NOT EXISTS Authors (AuthorName VARCHAR(255) PRIMARY KEY, Nationality VARCHAR(255), BirthDate DATE)")

# Tạo bảng Genres
cursor.execute("CREATE TABLE IF NOT EXISTS Genres (GenreName VARCHAR(255) PRIMARY KEY, Description TEXT)")

# Tạo bảng Books
cursor.execute("CREATE TABLE IF NOT EXISTS Books (BookID INT PRIMARY KEY, Title VARCHAR(255), AuthorName VARCHAR(255), GenreName VARCHAR(255), PublishYear INT, Price DECIMAL(10,2),Image LONGBLOB ,FOREIGN KEY (AuthorName) REFERENCES Authors(AuthorName), FOREIGN KEY (GenreName) REFERENCES Genres(GenreName))")


# Đóng kết nối MySQL
mydb.close()