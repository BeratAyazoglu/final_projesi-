from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gizli_anahtar'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ----------------------
# DB
# ----------------------

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)  
    last_name = db.Column(db.String(150), nullable=False)   
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    stocks = db.relationship('Stock', backref='owner', lazy=True)


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(100), nullable=False)
    manufacturer = db.Column(db.String(100), nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @property
    def kdvli_fiyat(self):
        return round(self.price * 1.18, 2)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ----------------------
# ANA SAYFA
# ----------------------

@app.route('/')
def home():
    return redirect(url_for('login'))  

# ----------------------
# KAYİT
# ----------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        existing_user = User.query.filter_by(email=request.form['email']).first()
        if existing_user:
            flash('Bu e-posta adresi zaten alınmış.', 'danger')
            return redirect(url_for('register'))

        hashed_pw = generate_password_hash(request.form['password'])
        user = User(
            first_name=request.form['first_name'],
            last_name=request.form['last_name'],
            email=request.form['email'],
            password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Kayıt başarılı, giriş yapıldı.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html')


# ----------------------
# GİRİS
# ----------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            flash('Giriş başarılı.', 'success')
            if user.is_admin:
                return redirect(url_for('admin_panel'))
            return redirect(url_for('dashboard'))
        else:
            flash('Hatalı e-posta veya şifre.', 'danger')
    return render_template('login.html')




# ----------------------
# CİKİS
# ----------------------

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Çıkış yapıldı.', 'info')
    return redirect(url_for('login'))

# ----------------------
# DASHBOARD 
# ----------------------

@app.route('/dashboard')
@login_required
def dashboard():
    q = request.args.get('q')
    if q:
        stocks = Stock.query.filter(
            Stock.user_id == current_user.id,
            (Stock.product_name.ilike(f"%{q}%")) | 
            (Stock.barcode.ilike(f"%{q}%")) |
            (Stock.manufacturer.ilike(f"%{q}%"))
        ).all()
    else:
        stocks = Stock.query.filter_by(user_id=current_user.id).all()
    
    return render_template('dashboard.html', user=current_user, stocks=stocks)

# ----------------------
# ADMİN PANEL 
# ----------------------

@app.route('/admin', methods=['GET'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Admin paneline erişim yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))

 
    search_query = request.args.get('search', '')
    role_filter = request.args.get('role', '')

    query = User.query

    if search_query:
        query = query.filter(
            (User.first_name.ilike(f'%{search_query}%')) |
            (User.last_name.ilike(f'%{search_query}%')) |
            (User.email.ilike(f'%{search_query}%'))
        )
    
    if role_filter == 'admin':
        query = query.filter(User.is_admin == True)
    elif role_filter == 'non-admin':
        query = query.filter(User.is_admin == False)

    users = query.all()
    
  
    stocks = Stock.query.all()
    return render_template('adminpanel.html', users=users, stocks=stocks)



# ----------------------
# STOK EKLEME
# ----------------------

@app.route('/stock/add', methods=['GET', 'POST'])
@login_required
def add_stock():
    if request.method == 'POST':
        print(request.form) 
        new_stock = Stock(
            product_name=request.form['product_name'],
            quantity=request.form['quantity'],
            price=request.form['price'],
            category=request.form['category'],
            barcode=request.form['barcode'],
            manufacturer=request.form.get('manufacturer', ''),
            owner=current_user
        )
        db.session.add(new_stock)
        db.session.commit()
        flash('Stok başarıyla eklendi.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('stokekle.html')


# ----------------------
# STOK DÜZENLEME
# ----------------------

@app.route('/edit_stock/<int:stock_id>', methods=['GET', 'POST'])
@login_required
def edit_stock(stock_id):
    stock = Stock.query.get_or_404(stock_id)
    if stock.user_id != current_user.id and not current_user.is_admin:
        flash('Bu stok üzerinde değişiklik yapma yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        stock.product_name = request.form['product_name']
        stock.quantity = request.form['quantity']
        stock.price = request.form['price']
        stock.manufacturer = request.form['manufacturer']
        stock.category = request.form['category']
        stock.barcode = request.form['barcode']
        db.session.commit()
        flash('Stok başarıyla güncellendi.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_stock.html', stock=stock)

# ----------------------
# STOK SİLME
# ----------------------
@app.route('/delete_stock/<int:stock_id>', methods=['POST'])
@login_required
def delete_stock(stock_id):
    stock = Stock.query.get_or_404(stock_id)
    if stock.user_id != current_user.id:
        flash('Bu stoğu silme yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(stock)
    db.session.commit()
    flash('Stok başarıyla silindi.', 'success')
    return redirect(url_for('dashboard'))

# ----------------------
# JSON DOSYASI
# ----------------------

@app.route('/export_json')
@login_required
def export_json():
    stocks = Stock.query.filter_by(user_id=current_user.id).all()
    data = []

    for stock in stocks:
        data.append({
            "id": stock.id,
            "product_name": stock.product_name,
            "quantity": stock.quantity,
            "price": float(stock.price),
            "kdvli_fiyat": float(stock.kdvli_fiyat),
            "manufacturer": stock.manufacturer,
            "category": stock.category,
            "barcode": stock.barcode,
            "created_at": stock.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(data)

# ----------------------
# ADMİN KULLANICI GİRİSİ
# ----------------------
def create_admin():
    admin_user = User.query.filter_by(email='admin@example.com').first()
    if not admin_user:
        admin_user = User(
            first_name='Admin',
            last_name='Admin',
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print('Admin kullanıcısı oluşturuldu.')

# ----------------------
# ADMİN PANEL İÇİN KULLANICI DÜZELTME
# ----------------------
@app.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin:
        flash('Admin yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.is_admin = 'is_admin' in request.form 
        db.session.commit()
        flash('Kullanıcı bilgileri güncellendi.', 'success')
        return redirect(url_for('admin_panel'))

    return render_template('edit_user.html', user=user)

# ----------------------
# KULLANICI SİLME
# ----------------------
@app.route('/admin/delete_user/<int:user_id>', methods=['GET'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Admin yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)

    if user == current_user:
        flash('Kendi hesabınızı silemezsiniz.', 'danger')
        return redirect(url_for('admin_panel'))

    db.session.delete(user)
    db.session.commit()
    flash('Kullanıcı başarıyla silindi.', 'success')
    return redirect(url_for('admin_panel'))

# ----------------------
# JSON DOSYASINA KAYIT
# ----------------------
@app.route('/save_json')
@login_required
def save_json():
    stocks = Stock.query.filter_by(user_id=current_user.id).all()

    data = [{
        "id": stock.id,
        "product_name": stock.product_name,
        "quantity": stock.quantity,
        "price": float(stock.price),
        "kdvli_fiyat": float(stock.kdvli_fiyat),
        "manufacturer": stock.manufacturer,
        "category": stock.category,
        "barcode": stock.barcode,
        "created_at": stock.created_at.strftime("%Y-%m-%d %H:%M:%S")
    } for stock in stocks]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    flash("Veriler 'data.json' dosyasına kaydedildi.", "success")
    return redirect(url_for('dashboard'))

# ----------------------
# KULLANICI  VERİLERİNİ AL
# ----------------------
@app.route('/manage_users')
@login_required
def manage_users():
    users = User.query.all()  
    return render_template('adminpanel.html', users=users)

# ----------------------
# VERİTABANI OLUŞTURMA
# ----------------------


if __name__ == '__main__':
    with app.app_context(): 
        if not os.path.exists('site.db'):
            db.create_all()
            create_admin()
            print("Veritabanı oluşturuldu.")
    
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

