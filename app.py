import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify
from Face_Recognition2 import face_recog
import cv2
import face_recognition
import os
import numpy as np
import threading

app = Flask(__name__)

# Kết nối đến cơ sở dữ liệu (hoặc tạo cơ sở dữ liệu mới nếu chưa tồn tại)
conn = sqlite3.connect('my_database.db')

# Tạo một đối tượng Cursor để thực hiện các truy vấn SQL
cursor = conn.cursor()

# Tạo bảng trong cơ sở dữ liệu
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    number INTEGER NOT NULL
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    number REAL NOT NULL
                )''')
# Lưu các thay đổi và đóng kết nối đến cơ sở dữ liệu
conn.commit()
conn.close()

@app.route('/api/data', methods=['POST'])
def store_data():
    data = request.json
    
    # Kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect('my_database.db')
    
    cursor = conn.cursor()
    
    # Thêm dữ liệu vào bảng
    cursor.execute("INSERT INTO products (name, price, number) VALUES (?, ?, ?)", (data['name'], data['price'], data['number']))
    
    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Data stored successfully"})

# @app.route('/')
# def home():
#     # Truy vấn tất cả sản phẩm từ cơ sở dữ liệu và hiển thị trên trang
#     conn = sqlite3.connect('my_database.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM products')
#     products = cursor.fetchall()
#     conn.close()
#     return render_template('index.html', products=products)
# sao link css không được nhỉ

@app.route('/')
def home():
    # Truy vấn tất cả sản phẩm từ cơ sở dữ liệu và hiển thị trên trang
    # conn = sqlite3.connect('my_database.db')
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM products')
    # products = cursor.fetchall()
    # conn.close()
    return render_template('login.html')



@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        # Lấy dữ liệu từ yêu cầu POST
        name = request.form['name']
        price = request.form['price']
        number = request.form['number']
        
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, price, number) VALUES (?, ?, ?)', (name, price, number))  # Sửa lỗi ở đây
        conn.commit()
        conn.close()
        return jsonify({"message": "Data received successfully"})
    
    # return redirect(url_for('index'))


@app.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Delete product successful"})

@app.route('/chatbot')
def render_chatbot():
    return render_template('chatbot.html')

@app.route('/customer')
def render_customer():
    return render_template('customer.html')

@app.route('/business')
def render_business():
    return render_template('business.html')

@app.route('/account')
def render_account():
    return render_template('account.html')

@app.route('/login')
def login_account():
    return render_template('login.html')

@app.route('/recognize')
def login_face_recognition():
    result,name = face_recog()
    if result == True:
        # Truy vấn tất cả sản phẩm từ cơ sở dữ liệu và hiển thị trên trang
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        conn.close()
        return render_template('index.html', noti=f"Xin chào {name}", products=products)
    else:
        # Nếu không nhận diện được khuôn mặt sau 5 giây, hiển thị thông báo thất bại
        threading.Timer(5.0, login_failure).start()

def login_failure():
    return "Đăng nhập thất bại"
    

if __name__ == '__main__':
    app.run(debug=True)
    
