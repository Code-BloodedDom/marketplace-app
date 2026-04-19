# Railway Deployment Guide

## Prerequisites
- Railway account (sign up at https://railway.app)
- GitHub account with repo or Railway CLI
- Stripe account (https://stripe.com)
- Gmail account with App Password for notifications

---

## Step 1: Setup Stripe API Keys

1. Go to **Stripe Dashboard** → https://dashboard.stripe.com/apikeys
2. Copy your **Publishable Key** (starts with `pk_`)
3. Copy your **Secret Key** (starts with `sk_`)
4. You'll need both for Railway environment variables

### For Testing (Development):
- Use test keys (starts with `pk_test_` and `sk_test_`)
- Test card: `4242 4242 4242 4242` with any future expiry and CVC

### For Production (Live):
- Use live keys (starts with `pk_live_` and `sk_live_`)
- Requires verification

---

## Step 2: Deploy to Railway

### Option A: Via GitHub (Recommended)

1. Push your code to GitHub:
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

2. Go to **Railway Dashboard** → https://railway.app/dashboard
3. Click **"+ New Project"** → **"Deploy from GitHub"**
4. Select your repository
5. Click **"Deploy"**

### Option B: Via Railway CLI

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Deploy:
```bash
cd marketplace_app
railway up
```

---

## Step 3: Configure Environment Variables on Railway

After deployment:

1. Go to **Railway Dashboard** → Select your project
2. Click **"Variables"** tab
3. Add these environment variables:

```
SECRET_KEY = (generate a long random string)
STRIPE_PUBLIC_KEY = pk_live_xxxxx
STRIPE_SECRET_KEY = sk_live_xxxxx
MAIL_USERNAME = your_email@gmail.com
MAIL_PASSWORD = your_app_password
FLASK_ENV = production
FLASK_DEBUG = False
```

### To Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Step 4: Add PostgreSQL Database

1. In **Railway Dashboard**, click **"+ New"** → **"Database"** → **"PostgreSQL"**
2. Create the database
3. Railway automatically sets `DATABASE_URL` environment variable
4. Your app will automatically use it!

---

## Step 5: Gmail App Password Setup

To enable email notifications:

1. Go to **Google Account Security** → https://myaccount.google.com/security
2. Enable **2-Factor Authentication** (if not already)
3. Create **App Password** for Gmail
4. Use this password (not your Gmail password) for `MAIL_PASSWORD`

---

## Step 6: Verify Deployment

1. Railway shows your app URL (e.g., `marketplace-app-production-xxxxx.railway.app`)
2. Click the URL to visit your live marketplace
3. Test user registration, login, and product upload
4. Test payments with Stripe test card

---

## Troubleshooting

### App not starting?
- Check **Logs** tab in Railway Dashboard
- Ensure all required environment variables are set
- Verify PostgreSQL database is connected

### Database connection error?
- Check if PostgreSQL plugin is attached
- Verify DATABASE_URL is set in Variables

### Payment not working?
- Confirm STRIPE_PUBLIC_KEY and STRIPE_SECRET_KEY are correct
- Check browser console for Stripe errors
- Use test keys for development

### Emails not sending?
- Verify MAIL_USERNAME and MAIL_PASSWORD are correct
- Check app logs for mail errors
- Gmail App Password must be used (not account password)

---

## Monitoring & Logs

View app logs in Railway:
1. Dashboard → Your Project → **Logs** tab
2. Check for errors in real-time

---

## Updates & Redeployment

To update your app:

```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

Railway automatically redeploys on GitHub push (if connected).

---

## Cost Estimates

- **Railway**: $5/month starting fee + pay-per-use
- **PostgreSQL**: Included with Railway plan
- **Stripe**: 2.9% + $0.30 per transaction

---

## Support

- Railway Docs: https://docs.railway.app
- Stripe Docs: https://stripe.com/docs
- Flask Docs: https://flask.palletsprojects.com
