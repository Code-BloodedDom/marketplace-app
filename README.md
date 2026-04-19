# School Marketplace

A comprehensive Flask-based school marketplace with real-time chat, user profiles, wishlists, and admin features.

## Features
- User registration and login (buyers/sellers)
- Product upload with image support
- Advanced search with filters (price, category, location, sorting)
- Product detail pages with reviews and ratings
- User profiles with bio, phone, location
- Wishlist for saving favorite products
- Real-time messaging between users (SocketIO)
- Admin dashboard for managing users and products
- Email notifications for new messages
- Mobile-responsive design
- Mock purchase system with orders and payments
- Seller analytics (sales, orders) with charts
- Product reporting for safety/moderation
- Order status updates (pending, paid, shipped, delivered)
- Location-based search (campus areas)
- Stripe payment integration
- Browser push notifications
- CSRF protection and rate limiting
- API endpoints for mobile app

## Mobile App
Basic React Native app in `mobile_app/` folder. Run with Expo:
```
npx expo install
npx expo start
```
Update API URL in App.js to your deployed Flask app.

## Setup
1. Open terminal in `marketplace_app`
2. Install dependencies:
   ```sh
   python -m pip install -r requirements.txt
   ```
3. Run the app:
   ```sh
   python app.py
   ```
4. Open http://127.0.0.1:5000 in your browser

## Deployment
For production deployment (e.g., Heroku):
1. Install Heroku CLI
2. Create Heroku app: `heroku create your-app-name`
3. Set environment variables:
   ```
   heroku config:set SECRET_KEY=your_secret_key
   heroku config:set MAIL_USERNAME=your_email@gmail.com
   heroku config:set MAIL_PASSWORD=your_password
   heroku config:set STRIPE_PUBLIC_KEY=pk_test_...
   heroku config:set STRIPE_SECRET_KEY=sk_test_...
   ```
4. For database, use Heroku Postgres: `heroku addons:create heroku-postgresql:hobby-dev`
5. Push to Heroku: `git push heroku main`
6. Open app: `heroku open`

## Database
- SQLite database `marketplace.db`
- Tables: User, Product, Review, Wishlist, Message, Category, Order, Payment, Report

## Email Notifications
- Configure `app.config['MAIL_USERNAME']` and `app.config['MAIL_PASSWORD']` for Gmail
- Or use another SMTP provider

## Security Notes
- Update `app.config['SECRET_KEY']` before deploying
- Use HTTPS in production
- Validate file uploads properly

## Mobile App
Basic React Native app in `mobile_app/` folder. Run with Expo:
```
npx expo install
npx expo start
```
Update API URL in App.js to your deployed Flask app.