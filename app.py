from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from models import db, User, Product, Review, Wishlist, Message, Category, Order, Payment, Report
from flask_mail import Mail, Message as MailMessage
from datetime import datetime
import stripe

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')

# Database configuration - handle both SQLite and PostgreSQL
database_url = os.environ.get('DATABASE_URL', 'sqlite:///marketplace.db')
# Fix PostgreSQL URI if needed (Railway uses postgres://, but SQLAlchemy 2.0+ needs postgresql://)
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Mail config (for notifications)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'your_email@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your_password')

# Stripe config
app.config['STRIPE_PUBLIC_KEY'] = os.environ.get('STRIPE_PUBLIC_KEY', 'pk_test_your_public_key')
app.config['STRIPE_SECRET_KEY'] = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_your_secret_key')
stripe.api_key = app.config['STRIPE_SECRET_KEY']

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

csrf = CSRFProtect(app)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

socketio = SocketIO(app)
mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("3 per minute")
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        is_seller = 'is_seller' in request.form
        user = User(username=username, email=email, password=password, is_seller=is_seller)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if not current_user.is_seller:
        flash('Only sellers can upload products')
        return redirect(url_for('home'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        price = float(request.form['price'])
        category = request.form['category']
        location = request.form.get('location')
        file = request.files.get('image')
        filename = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        product = Product(title=title, description=description, price=price, category=category, location=location, image=filename, seller_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        flash('Product uploaded!')
        return redirect(url_for('home'))
    return render_template('upload.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    location = request.args.get('location', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'newest')
    products = Product.query
    if query:
        products = products.filter(Product.title.contains(query) | Product.description.contains(query))
    if category:
        products = products.filter_by(category=category)
    if location:
        products = products.filter(Product.location.contains(location))
    if min_price is not None:
        products = products.filter(Product.price >= min_price)
    if max_price is not None:
        products = products.filter(Product.price <= max_price)
    if sort_by == 'price_low':
        products = products.order_by(Product.price)
    elif sort_by == 'price_high':
        products = products.order_by(Product.price.desc())
    else:
        products = products.order_by(Product.created_at.desc())
    products = products.all()
    return render_template('search.html', products=products, query=query, category=category, location=location, min_price=min_price, max_price=max_price, sort_by=sort_by)

@app.route('/product/<int:id>')
def product(id):
    product = Product.query.get_or_404(id)
    reviews = Review.query.filter_by(product_id=id).all()
    return render_template('product.html', product=product, reviews=reviews)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.bio = request.form.get('bio')
        current_user.phone = request.form.get('phone')
        current_user.location = request.form.get('location')
        file = request.files.get('profile_pic')
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_pic = filename
        db.session.commit()
        flash('Profile updated!')
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/wishlist')
@login_required
def wishlist():
    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', wishlist=wishlist_items)

@app.route('/add_to_wishlist/<int:product_id>')
@login_required
def add_to_wishlist(product_id):
    if not Wishlist.query.filter_by(user_id=current_user.id, product_id=product_id).first():
        wishlist_item = Wishlist(user_id=current_user.id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        flash('Added to wishlist!')
    return redirect(url_for('product', id=product_id))

@app.route('/messages')
@login_required
def messages():
    conversations = db.session.query(Message.receiver_id, User.username).filter(
        Message.sender_id == current_user.id).distinct().all()
    received = db.session.query(Message.sender_id, User.username).filter(
        Message.receiver_id == current_user.id).distinct().all()
    all_convos = set(conversations + received)
    return render_template('messages.html', conversations=all_convos)

@app.route('/chat/<int:user_id>', methods=['GET', 'POST'])
@login_required
def chat(user_id):
    other_user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        content = request.form['content']
        message = Message(sender_id=current_user.id, receiver_id=user_id, content=content)
        db.session.add(message)
        db.session.commit()
        # Send email notification
        if other_user.email:
            msg = MailMessage('New Message', sender=app.config['MAIL_USERNAME'], recipients=[other_user.email])
            msg.body = f'You have a new message from {current_user.username}: {content}'
            mail.send(msg)
        return redirect(url_for('chat', user_id=user_id))
    msgs = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.timestamp).all()
    return render_template('chat.html', other_user=other_user, messages=msgs)

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_seller:  # Assume admin is seller for now
        flash('Access denied')
        return redirect(url_for('home'))
    users = User.query.all()
    products = Product.query.all()
    reports = Report.query.all()
    return render_template('admin.html', users=users, products=products, reports=reports)

@app.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    if not current_user.is_seller:
        flash('Access denied')
        return redirect(url_for('home'))
    product = Product.query.get_or_404(id)
    if product.seller_id != current_user.id:
        flash('Not your product')
        return redirect(url_for('home'))
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted')
    return redirect(url_for('admin'))

@app.route('/buy/<int:product_id>', methods=['GET', 'POST'])
@login_required
def buy(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        quantity = int(request.form['quantity'])
        total = product.price * quantity
        # Create order
        order = Order(buyer_id=current_user.id, product_id=product_id, quantity=quantity, total_price=total)
        db.session.add(order)
        db.session.commit()
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': product.title,
                    },
                    'unit_amount': int(product.price * 100),  # Stripe expects cents
                },
                'quantity': quantity,
            }],
            mode='payment',
            success_url=url_for('payment_success', order_id=order.id, _external=True),
            cancel_url=url_for('payment_cancel', _external=True),
        )
        return redirect(session.url, code=303)
    return render_template('buy.html', product=product, stripe_public_key=app.config['STRIPE_PUBLIC_KEY'])

@app.route('/orders')
@login_required
def orders():
    if current_user.is_seller:
        orders = Order.query.join(Product).filter(Product.seller_id == current_user.id).all()
    else:
        orders = Order.query.filter_by(buyer_id=current_user.id).all()
    return render_template('orders.html', orders=orders)

@app.route('/analytics')
@login_required
def analytics():
    if not current_user.is_seller:
        flash('Access denied')
        return redirect(url_for('home'))
    products = Product.query.filter_by(seller_id=current_user.id).all()
    total_sales = db.session.query(db.func.sum(Order.total_price)).join(Product).filter(Product.seller_id == current_user.id).scalar() or 0
    total_orders = db.session.query(Order).join(Product).filter(Product.seller_id == current_user.id).count()
    # Simple sales data (last 7 days)
    from datetime import timedelta
    sales_data = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        sales = db.session.query(db.func.sum(Order.total_price)).join(Product).filter(
            Product.seller_id == current_user.id,
            Order.created_at >= date.replace(hour=0, minute=0, second=0),
            Order.created_at < (date + timedelta(days=1)).replace(hour=0, minute=0, second=0)
        ).scalar() or 0
        sales_data.append({'date': date.strftime('%Y-%m-%d'), 'sales': sales})
    sales_data.reverse()
    labels = [d['date'] for d in sales_data]
    data = [d['sales'] for d in sales_data]
    return render_template('analytics.html', products=products, total_sales=total_sales, total_orders=total_orders, labels=labels, data=data)

@app.route('/report/<int:product_id>', methods=['GET', 'POST'])
@login_required
def report_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        reason = request.form['reason']
        report = Report(reporter_id=current_user.id, product_id=product_id, reason=reason)
        db.session.add(report)
        db.session.commit()
        flash('Report submitted')
        return redirect(url_for('product', id=product_id))
    return render_template('report.html', product=product)

@app.route('/payment_success/<int:order_id>')
@login_required
def payment_success(order_id):
    order = Order.query.get_or_404(order_id)
    if order.buyer_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('home'))
    order.status = 'paid'
    payment = Payment(order_id=order.id, amount=order.total_price, status='completed')
    db.session.add(payment)
    db.session.commit()
    flash('Payment successful! Order confirmed.')
    return redirect(url_for('orders'))

@app.route('/payment_cancel')
@login_required
def payment_cancel():
    flash('Payment cancelled.')
    return redirect(url_for('home'))

@app.route('/api/products')
def api_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'price': p.price,
        'image': url_for('static', filename='uploads/' + p.image, _external=True) if p.image else None
    } for p in products])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add default categories
        if not Category.query.first():
            categories = ['Books', 'Electronics', 'Clothing', 'Furniture', 'Sports', 'Other']
            for cat in categories:
                db.session.add(Category(name=cat))
            db.session.commit()
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, use_reloader=False)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{current_user.username} has entered the room.'}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    msg = data['msg']
    emit('message', {'msg': msg, 'user': current_user.username}, room=room)
    # Save to db
    receiver_id = int(room.split('_')[1]) if room.startswith(str(current_user.id)) else int(room.split('_')[0])
    message = Message(sender_id=current_user.id, receiver_id=receiver_id, content=msg)
    db.session.add(message)
    db.session.commit()