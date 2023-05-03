from flask import Flask, url_for, redirect, session, request, render_template
from db_config import mydb, cursor
import base64


app = Flask(__name__)
app.secret_key = "Dungdz1st"

@app.route('/')
def index():
    product_id = request.args.get('product_id')
    if product_id != None:
        cursor.execute(
            f'SELECT * FROM product WHERE product_id LIKE "%{product_id}%"')
    else:
        cursor.execute('SELECT * FROM product')
        products = cursor.fetchall()
    return render_template('home.html', products=products, len=len(products), base64=base64)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
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
                img_data = img.read()
                img_pil = Image.open(io.BytesIO(img_data))
                img_buffer = io.BytesIO()
                img_pil.save(img_buffer, format='JPEG')
                img_binary = img_buffer.getvalue()
            # Thêm sản phẩm vào cơ sở dữ liệu
            sql = f'INSERT INTO product VALUES ({product_id}, "{product_name}", "{description}", {price}, %s, {quantity})'
            cursor.execute(sql, (img_binary,))
            mydb.commit()
    return redirect('/')



@app.route('/products')
def products():
    # Truy vấn cơ sở dữ liệu để lấy các bản ghi sản phẩm
    cursor.execute("SELECT * FROM product")
    products = cursor.fetchall()
    # Trả về mẫu Jinja2 và truyền danh sách sản phẩm vào
    return render_template('products.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)