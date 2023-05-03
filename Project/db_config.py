import mysql.connector

# Kết nối đến csdl qlsv
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='qls'
)

# Tạo đối tượng cursor() để thao tác với csdl qlsv
cursor = mydb.cursor()
