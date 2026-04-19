# School Marketplace

A starter Flask application for a student marketplace. Students can register as buyers or sellers, upload products, search listings, and leave reviews.

## Features
- User registration and login
- Buyer and seller roles
- Product upload with image support
- Search by keyword and category
- Product detail pages with reviews

## Setup
1. Open a terminal in `marketplace_app`
2. Install dependencies:
   ```sh
   python -m pip install -r requirements.txt
   ```
3. Run the app:
   ```sh
   python app.py
   ```
4. Open http://127.0.0.1:5000 in your browser

## Notes
- Uploaded images are stored in `static/uploads`
- The database file is `marketplace.db`
- Update `app.config['SECRET_KEY']` before deploying

## Next steps
- Add user profiles and messaging
- Add product categories and filters
- Add payment or escrow flow
- Add mobile-friendly responsive design
