from flask import Flask, url_for, redirect, session, request, render_template
from db_config import mydb, cursor
from PIL import Image
import io
import base64


app = Flask(__name__)
app.secret_key = "Dungdz1st"


@app.route('/')
def home():
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    role = session.get('role')
    return render_template('index.html', products=products, len=len(products), base64=base64, get_user_fullname=get_user_fullname, role= role)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        password = request.form.get('password')
        sql = f'INSERT INTO users (phone_number, email, full_name, password, role)  VALUES ("{phone_number}", "{email}", "{full_name}", "{password}", "member"  )'
        cursor.execute(sql)
        mydb.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        password = request.form.get('password')
        sql = 'SELECT * FROM users WHERE phone_number = %s AND password = %s'
        cursor.execute(sql, (phone_number, password))
        user = cursor.fetchone()
        if user:
            role = user[4]
            session['role'] = role
            session['phone_number'] = user[0]
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='sai')
    return render_template('login.html')

def get_user_fullname(phone_number):
    cursor.execute('SELECT full_name FROM users WHERE phone_number = %s', (phone_number,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return 'Người dùng'
    
@app.route('/logout/')
def logout():
    # remove the user session variables
    session.pop('role', None)
    session.pop('phone_number', None)
    # redirect to the login page
    return redirect(url_for('login'))


@app.route('/crud')
def crud():
    product_name = request.args.get('product_name')
    if product_name != None:
        cursor.execute(
            f'SELECT * FROM product WHERE product_name LIKE "%{product_name}%"')
    else:
        cursor.execute('SELECT * FROM product')
    products = cursor.fetchall()
    return render_template('crud.html', products=products, len=len(products) ,base64=base64)



@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        description = request.form.get('description')
        price = request.form.get('price')
        img = request.files.get('img')
        quantity = request.form.get('quantity')
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
        # Thêm sản phẩm vào cơ sở dữ liệu
        sql = f'INSERT INTO product (product_id, product_name, description, price, img, quantity) VALUES (%s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (product_id, product_name, description, price, img_binary, quantity))
        mydb.commit()
    return redirect('/crud')

   
@app.route('/update', methods=['GET', 'POST'])
def updateProduct():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        product_name = request.form.get('product_name')
        description = request.form.get('description')
        price = request.form.get('price')
        img = request.files.get('img')
        quantity = request.form.get('quantity')
        img_binary = None
        if img:
            img_file = request.files['img']
            img_data = img_file.read()
            img_pil = Image.open(io.BytesIO(img_data))
            img_buffer = io.BytesIO()
            img_pil.save(img_buffer, format='JPEG')
            img_binary = img_buffer.getvalue()
            img_base64 = base64.b64encode(img_data)
        sql = 'UPDATE product SET product_name = %s, description = %s, price = %s, img = %s, quantity = %s WHERE product_id = %s'
        val = (product_name, description, price, img_binary, quantity, product_id)
        cursor.execute(sql, val)
        mydb.commit()
    return redirect('/crud')


@app.route('/delete/<product_id>')
def deleteProduct(product_id):
    sql = f'DELETE FROM product WHERE product_id = {product_id}'
    cursor.execute(sql)
    mydb.commit()
    return redirect('/crud') 


@app.route('/products')
def products():
    # Truy vấn cơ sở dữ liệu để lấy các bản ghi sản phẩm
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    # Trả về mẫu Jinja2 và truyền danh sách sản phẩm vào
    return render_template('product.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)