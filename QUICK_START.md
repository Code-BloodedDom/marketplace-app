# 🚀 QUICK DEPLOYMENT CHECKLIST

## Before You Deploy ✅

- [ ] GitHub repository created with code pushed
- [ ] Stripe account created (https://stripe.com)
- [ ] Stripe API keys copied (test keys for dev)
- [ ] Gmail account with 2FA enabled
- [ ] Gmail App Password generated for notifications
- [ ] Railway account created (https://railway.app)

---

## Deploy in 5 Steps

### 1️⃣ Push Code to GitHub
```bash
cd marketplace_app
git add .
git commit -m "Ready for production"
git push origin main
```

### 2️⃣ Deploy to Railway (2 min)
- Go to https://railway.app/dashboard
- Click **"+ New Project"** → **"Deploy from GitHub"**
- Select your repository
- Click **"Deploy"**

### 3️⃣ Add PostgreSQL Database (1 min)
- In Railway: **"+ New"** → **"Database"** → **"PostgreSQL"**
- Railway auto-sets `DATABASE_URL`

### 4️⃣ Set Environment Variables (2 min)
In Railway Variables tab, add:
```
SECRET_KEY = (use: python -c "import secrets; print(secrets.token_hex(32))")
STRIPE_PUBLIC_KEY = pk_test_xxxxx (from Stripe Dashboard)
STRIPE_SECRET_KEY = sk_test_xxxxx (from Stripe Dashboard)
MAIL_USERNAME = your_email@gmail.com
MAIL_PASSWORD = your_app_password (from Gmail)
FLASK_ENV = production
```

### 5️⃣ Verify Deployment (1 min)
- Check Railway logs for errors
- Click your app URL
- Login and test a payment with `4242 4242 4242 4242`
- ✅ Live!

---

## Environment Variables Explained

| Variable | Value | Source |
|----------|-------|--------|
| `SECRET_KEY` | Long random string | Generate with `secrets` module |
| `STRIPE_PUBLIC_KEY` | `pk_test_...` | Stripe Dashboard → Developers → API Keys |
| `STRIPE_SECRET_KEY` | `sk_test_...` | Stripe Dashboard → Developers → API Keys |
| `DATABASE_URL` | Auto-set by Railway | Add PostgreSQL plugin |
| `MAIL_USERNAME` | your@gmail.com | Gmail account |
| `MAIL_PASSWORD` | App Password | Google Account → Security → App Passwords |
| `FLASK_ENV` | `production` | Set for production |

---

## Test Payment Card (Development Only)

| Field | Value |
|-------|-------|
| Card Number | `4242 4242 4242 4242` |
| Expiry | `12/25` (any future date) |
| CVC | `123` (any 3 digits) |
| Name | Any name |

---

## Important Links

- 🛣️ **Railway Dashboard**: https://railway.app/dashboard
- 💳 **Stripe Dashboard**: https://dashboard.stripe.com
- 📧 **Gmail Security**: https://myaccount.google.com/security
- 📚 **Deployment Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🔐 **Stripe Setup**: [STRIPE_SETUP.md](STRIPE_SETUP.md)

---

## Troubleshooting

### App won't start?
→ Check Railway **Logs** tab for errors  
→ Verify all environment variables are set  
→ Check if PostgreSQL database is connected

### Payment not working?
→ Verify Stripe keys are correct  
→ Use test keys (`pk_test_`, `sk_test_`)  
→ Use test card: `4242 4242 4242 4242`

### Emails not sending?
→ Verify Gmail App Password (not account password)  
→ Check app logs for mail errors  
→ Ensure 2FA is enabled on Gmail

---

## After Deployment

1. **Monitor**: Check Railway logs daily for errors
2. **Iterate**: Push code updates, Railway auto-redeploys
3. **Scale**: Add more resources if needed
4. **Go Live**: Switch Stripe from test to live keys when ready

---

## Support & Resources

- **Railway Docs**: https://docs.railway.app
- **Stripe Docs**: https://stripe.com/docs  
- **Flask Docs**: https://flask.palletsprojects.com
- **Issues?** Check [DEPLOYMENT.md](DEPLOYMENT.md) troubleshooting section

---

**Your marketplace is production-ready! 🎉**

Questions? Read DEPLOYMENT.md or STRIPE_SETUP.md
