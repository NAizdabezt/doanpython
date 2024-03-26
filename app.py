from flask import Flask, render_template, request, redirect, session, url_for, jsonify, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from templates.models import db
from templates.models import Product 


app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:12345678@localhost/my_database?charset=utf8mb4'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.permanent_session_lifetime = timedelta(minutes=10)
db = SQLAlchemy(app=app)

# Tạo một engine để kết nối đến cơ sở dữ liệu
engine = create_engine('mysql+pymysql://root:12345678@localhost/my_database?charset=utf8mb4')

# Tạo một sessionmaker để tạo session
Session = sessionmaker(bind=engine)


# # Thiết lập điều kiện chuyển hướng trước mỗi request
# @app.before_request
# def require_login():
#     if 'logged_in' not in session and request.endpoint not in ['login', 'static']:
#         return redirect(url_for('login'))
        
@app.route('/')
def log():
    return render_template("home.html")

# Route để lưu dữ liệu từ biểu mẫu
@app.route('/api/data', methods=['POST'])
def store_data():
    data = request.json
    product = Product(name=data['name'], price=data['price'], quantity=data['quantity'])
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Data stored successfully"})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session.permanent = True
        con, cursor = connect_db()
        cursor.execute('SELECT * FROM staffaccounts WHERE account=? AND password=?', (username, password))
        match = cursor.fetchone()
        con.close()
        if match:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')  # Thêm thông điệp lỗi vào flash
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def log_out():
    session.pop("logged_in",False)
    return redirect(url_for("login"))

@app.route('/index')
def index():
    if 'logged_in' in session and session['logged_in']:
        # Đã đăng nhập, chuyển hướng đến trang index hoặc trang chính của ứng dụng
        return render_template('index.html')  # hoặc chuyển hướng đến trang chính của ứng dụng
    else:
        # Chưa đăng nhập, chuyển hướng đến trang đăng nhập
        return redirect(url_for('login'))
        
# Route chính để hiển thị trang chính và danh sách sản phẩm
@app.route('/home')
def home():
    # Tạo một session để truy vấn cơ sở dữ liệu
    session = Session()

    # Truy vấn cơ sở dữ liệu để lấy danh sách sản phẩm
    products = session.query(Product).all()

    # Đóng session sau khi sử dụng
    session.close()

    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        # Lấy dữ liệu từ yêu cầu POST
        id = int(request.form['id'])
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        # Kiểm tra xem sản phẩm đã tồn tại trong cơ sở dữ liệu chưa
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
        existing_product = cursor.fetchone()
        conn.close()

        if existing_product:
            # Sản phẩm đã tồn tại, tăng số lượng
            new_quantity = existing_product[3] + quantity
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_quantity, id))
            conn.commit()
            conn.close()
            return redirect(url_for('home'))
        else:
            # Sản phẩm chưa tồn tại, thêm hàng mới
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)', (id, name, price, quantity))
            conn.commit()
            conn.close()
                
            return redirect(url_for('home'))
    
    return redirect(url_for('index'))


# Route để xóa sản phẩm
@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    conn, cursor = connect_db()
    cursor.execute('DELETE FROM products WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product deleted successfully"})

# Route để kiểm tra sự trùng lặp dựa trên ID và tên
@app.route('/check_duplicate', methods=['POST'])
def check_duplicate():
    data = request.json
    id = data['id']
    name = data['name']
    product = Product.query.filter_by(id=id, name=name).first()
    
    duplicate = False
    matching_name = False
    
    if product:
        duplicate = True
        matching_name = True
    
    return jsonify({"duplicate": duplicate, "matchingName": matching_name})

# Route để tăng số lượng của sản phẩm đã tồn tại
@app.route('/increase_quantity/<int:id>', methods=['POST'])
def increase_quantity(id):
    data = request.json
    quantity = data['quantity']
    
    product = Product.query.get(id)
    if product:
        product.quantity += quantity
        db.session.commit()
        return jsonify({"message": "Quantity increased successfully"})
    else:
        return jsonify({"error": "Product not found"}), 404

# Route để tự động điền Name và Price khi nhập ID
@app.route('/get_product_info/<int:id>', methods=['GET'])
def get_product_info(id):
    product = Product.query.get(id)
    if product:
        return jsonify({"id": id, "name": product.name, "price": product.price})
    else:
        return jsonify({"error": "Product not found", "id": id, "name": "", "price": ""}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

print("Halo")