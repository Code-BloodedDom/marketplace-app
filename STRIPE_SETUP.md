# Stripe Setup Guide for Student Marketplace

## What is Stripe?

Stripe is a payment processor that allows students to buy/sell products securely. It handles credit card processing, security, and payments.

---

## Getting Your Stripe Keys (5 minutes)

### Step 1: Create Stripe Account

1. Go to https://stripe.com
2. Click **"Sign up"**
3. Enter email and password
4. Verify your email
5. Complete your account details

### Step 2: Get Your API Keys

1. Log in to **Stripe Dashboard**: https://dashboard.stripe.com
2. Click **"Developers"** (left sidebar)
3. Click **"API Keys"** (second left sidebar)
4. You'll see:
   - **Publishable Key** (starts with `pk_test_` or `pk_live_`)
   - **Secret Key** (starts with `sk_test_` or `sk_live_`)

### For Testing (Development):
- Stripe automatically gives you **Test Mode** keys
- Toggle **"View Test Data"** at the top to see test mode
- Test Card: `4242 4242 4242 4242`
- Expiry: Any future date (e.g., 12/25)
- CVC: Any 3 digits (e.g., 123)

### For Live (Production):
- Requires ID verification
- Keep Secret Key private (never share!)
- Switch "Test Mode" toggle to activate Live keys

---

## Copy Your Keys to Railway

1. Go to **Railway Dashboard** → Your Project
2. Click **"Variables"** tab
3. Add:
   ```
   STRIPE_PUBLIC_KEY = pk_test_xxxxxxxxxxxxx
   STRIPE_SECRET_KEY = sk_test_xxxxxxxxxxxxx
   ```
4. Click **"Deploy"** to update your app

---

## Testing Payments in Your App

1. Visit your marketplace app
2. Login as a student
3. Click **"Buy"** on a product
4. Enter test card: `4242 4242 4242 4242`
5. Expiry: `12/25` (any future date)
6. CVC: `123` (any 3 digits)
7. Click **"Pay"** → Should see success message!

---

## Webhook Setup (Advanced)

To get payment notifications in your app:

1. **Stripe Dashboard** → **Developers** → **Webhooks**
2. Click **"Add endpoint"**
3. Endpoint URL: `https://your-railway-url.railway.app/stripe-webhook`
4. Select events:
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
5. Get **Signing Secret** and add to Railway Variables as `STRIPE_WEBHOOK_SECRET`

---

## Fees

- **Stripe Charge**: 2.9% + $0.30 per transaction
- **You Set Price**: Student sets product price
- **Platform Fee** (Optional): Take percentage of each sale

Example:
- Product Price: $50
- Stripe Fee: $1.75 (2.9% + $0.30)
- Your Fee (if 5%): $2.50
- Student Gets: $45.75

---

## Security Checklist

✅ Never share Secret Key  
✅ Keep API keys in environment variables  
✅ Use Test keys for development  
✅ Use Live keys only in production  
✅ Enable 2FA on Stripe account  
✅ Verify student IDs for payouts  

---

## Dashboard Monitoring

Monitor payments in real-time:

1. **Stripe Dashboard** → **Payments**
2. See all transactions
3. View refunds and disputes
4. Check payout schedule

---

## Common Issues

**"Invalid API Key" error?**
- Verify key is correct (no spaces)
- Check if using Test vs Live key mismatch
- Ensure Railway variables are updated

**Payment declined?**
- Check test card number
- Verify expiry date is in future
- Use test mode keys (pk_test_, sk_test_)

**Not seeing transactions?**
- Ensure Test Mode toggle is OFF for live transactions
- Check Stripe Dashboard Payments tab
- Verify webhook is configured

---

## Next Steps

1. ✅ Create Stripe Account
2. ✅ Copy API Keys
3. ✅ Add Keys to Railway Variables
4. ✅ Deploy App
5. ✅ Test payment with test card
6. ✅ Go live with real payments!

For help: https://stripe.com/support
