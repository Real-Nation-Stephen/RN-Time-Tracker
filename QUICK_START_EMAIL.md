# 📧 Quick Start: Email Alerts

## 🚀 3-Minute Setup

### Step 1: Get Gmail App Password
1. Go to https://myaccount.google.com/security
2. Enable "2-Step Verification" if not already on
3. Click "App passwords"
4. Select "Mail" → "Other" → Enter "RN Time Tracker"
5. Copy the 16-character password

### Step 2: Add to Secrets
Create `.streamlit/secrets.toml` in your project folder:

```toml
[GMAIL_SMTP_SETTINGS]
email = "your-email@gmail.com"
app_password = "paste-your-app-password-here"
smtp_server = "smtp.gmail.com"
smtp_port = 587
```

### Step 3: Test It!
```bash
python test_email.py
```

You should see:
```
✅ SUCCESS! Email sent successfully!
```

---

## 📱 How to Use

### Manual Email (From Dashboard)
1. Open the app: `streamlit run rn_time_tracker.py`
2. Login as admin (Kay or Stephen)
3. Go to **Dashboard** tab
4. Click **📧 Send Weekly Alert**
5. Check Kay's email!

### Automatic Weekly Emails
Run the scheduler in the background:
```bash
nohup python email_scheduler.py > email_scheduler.log 2>&1 &
```

Sends every **Friday at 4:00 PM** automatically!

---

## 📊 What's in the Email?

✅ **Standard Projects Summary**
- Hours logged per user
- Entry counts
- Project counts
- Submission status

✅ **AIB Future Sparks Summary**
- AIBFS hours logged
- Suite breakdowns
- Status per user

✅ **Missing Submissions Alert**
- Who hasn't submitted
- Easy follow-up

---

## 🔧 Common Issues

### "Email settings not configured"
→ Add SMTP settings to `.streamlit/secrets.toml`

### "Authentication failed"
→ Use **App Password**, not regular password
→ Regenerate app password if needed

### Email not arriving
→ Check spam folder
→ Verify recipient: `kay.mckeon@realnation.ie`

---

## 📖 Need More Help?
See detailed guide: **EMAIL_SETUP.md**

---

**Quick Test:** `python test_email.py`
**Check Logs:** `tail -f email_scheduler.log`
**Stop Scheduler:** `pkill -f email_scheduler.py`

