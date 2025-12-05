# 📧 Email Alert Setup Guide

## Overview
The RN Time Tracker can send automated weekly email reports to Kay with a comprehensive summary of all team members' time tracking submissions.

## Features
- **📊 Comprehensive Reports**: Includes both Standard Projects and AIB Future Sparks data
- **👥 User Summary**: Shows hours logged, entries count, and submission status per user
- **⚠️ Missing Alerts**: Highlights users who haven't submitted their time
- **📅 Automatic Scheduling**: Can run automatically every Friday at 4:00 PM
- **🎨 Professional HTML**: Beautiful, easy-to-read email format

---

## 🔧 Setup Instructions

### Step 1: Configure SMTP Settings

You need to add Gmail SMTP settings to your Streamlit secrets. There are two ways to do this:

#### Option A: Local Development (`.streamlit/secrets.toml`)

Create/edit the file `.streamlit/secrets.toml` in your project root:

```toml
# Gmail SMTP Settings for Email Alerts
[GMAIL_SMTP_SETTINGS]
email = "your-email@gmail.com"
app_password = "your-app-password-here"
smtp_server = "smtp.gmail.com"
smtp_port = 587
```

#### Option B: Streamlit Cloud Deployment

1. Go to your app settings in Streamlit Cloud
2. Navigate to "Secrets" section
3. Add the following:

```toml
[GMAIL_SMTP_SETTINGS]
email = "your-email@gmail.com"
app_password = "your-app-password-here"
smtp_server = "smtp.gmail.com"
smtp_port = 587
```

### Step 2: Generate Gmail App Password

**Important:** You CANNOT use your regular Gmail password. You must create an App Password:

1. Go to your Google Account: https://myaccount.google.com/
2. Select **Security** from the left menu
3. Under "Signing in to Google", enable **2-Step Verification** (if not already enabled)
4. Once 2-Step Verification is on, select **App passwords**
5. Click **Select app** → Choose "Mail"
6. Click **Select device** → Choose "Other" and enter "RN Time Tracker"
7. Click **Generate**
8. Copy the 16-character password (it will look like: `xxxx xxxx xxxx xxxx`)
9. Paste this password (without spaces) into your secrets as `app_password`

---

## 🧪 Testing the Email Function

### Method 1: Manual Test from Dashboard (Recommended)

1. Launch the Time Tracker app:
   ```bash
   streamlit run rn_time_tracker.py
   ```

2. Log in with an **admin account** (Kay or Stephen)

3. Navigate to the **Dashboard** tab

4. Scroll down to the "Export Options" section

5. Click the **📧 Send Weekly Alert** button

6. If configured correctly, you should see:
   - ✅ "Weekly email alert sent!"
   - Check Kay's inbox for the email

7. If there's an error:
   - ❌ Check the terminal output for detailed error messages
   - Verify SMTP settings are correct
   - Ensure app password is valid

### Method 2: Test from Command Line

```python
# test_email.py
from rn_time_tracker import TimeTrackerApp

app = TimeTrackerApp()
success = app.send_weekly_email_alert()

if success:
    print("✅ Email sent successfully!")
else:
    print("❌ Email failed to send. Check error messages above.")
```

Run: `python test_email.py`

---

## 🤖 Automated Weekly Scheduling

### Setup Automatic Friday Emails

The `email_scheduler.py` script sends reports every Friday at 4:00 PM.

#### Option 1: Run in Background (Mac/Linux)

```bash
# Start the scheduler in the background
nohup python email_scheduler.py > email_scheduler.log 2>&1 &

# Check if it's running
ps aux | grep email_scheduler

# View logs
tail -f email_scheduler.log

# Stop the scheduler
pkill -f email_scheduler.py
```

#### Option 2: Use System Scheduler (Mac - LaunchDaemon)

Create file: `~/Library/LaunchAgents/com.realnation.timetracker.email.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.realnation.timetracker.email</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/realnation/Desktop/RN-Time-Tracker/email_scheduler.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/realnation/Desktop/RN-Time-Tracker/email_scheduler.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/realnation/Desktop/RN-Time-Tracker/email_scheduler_error.log</string>
</dict>
</plist>
```

Then activate:
```bash
launchctl load ~/Library/LaunchAgents/com.realnation.timetracker.email.plist
launchctl start com.realnation.timetracker.email
```

#### Option 3: Use Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add this line (runs every Friday at 4:00 PM)
0 16 * * 5 cd /Users/realnation/Desktop/RN-Time-Tracker && /usr/bin/python3 email_scheduler.py >> email_scheduler.log 2>&1
```

#### Option 4: Server/Cloud Deployment

For production, consider using:
- **Heroku Scheduler** (if hosting on Heroku)
- **AWS EventBridge** (if using AWS)
- **Google Cloud Scheduler** (if using GCP)
- **Dedicated server with systemd** (Linux)

---

## 📋 Email Report Contents

The weekly email includes:

### Header Section
- 📅 Week date range
- 👥 Expected users count
- ✅ Number of submissions received
- ⏰ Report generation timestamp

### Standard Projects Table
For each user:
- Total hours logged
- Number of entries
- Number of unique projects
- ✅/❌ Submission status

### AIB Future Sparks Table (if applicable)
For each user with AIBFS entries:
- Total AIBFS hours
- Number of AIBFS entries
- Number of unique suites
- Status indicator

### Missing Submissions Alert
- ⚠️ List of users who haven't submitted
- Helps identify who needs follow-up

---

## 🔍 Troubleshooting

### "Email settings not configured"
**Problem:** SMTP settings not found in secrets

**Solution:**
1. Check `.streamlit/secrets.toml` exists
2. Verify the `[GMAIL_SMTP_SETTINGS]` section is present
3. Restart the Streamlit app after adding secrets

### "Authentication failed"
**Problem:** Gmail rejecting login

**Solution:**
1. Verify you're using an **App Password**, not your regular password
2. Check the app password is entered without spaces
3. Ensure 2-Step Verification is enabled on your Google Account
4. Try generating a new app password

### "Connection refused" or "Timeout"
**Problem:** Can't connect to Gmail SMTP server

**Solution:**
1. Check your internet connection
2. Verify firewall isn't blocking port 587
3. Try `smtp_port = 465` with SSL instead
4. Check if your network blocks SMTP

### Email not arriving
**Problem:** No error but email doesn't arrive

**Solution:**
1. Check Kay's spam/junk folder
2. Verify recipient email: `kay.mckeon@realnation.ie`
3. Check Gmail "Sent" folder to confirm it was sent
4. Try sending to a different email address for testing

### "No data available for email report"
**Problem:** No time entries found for the week

**Solution:**
1. Verify users have submitted time entries
2. Check the date range (current week Monday-Sunday)
3. Confirm entries are in Google Sheets
4. Check Google Sheets connection is working

---

## 📝 Customization

### Change Email Recipient

Edit `rn_time_tracker.py`, line ~1760:

```python
msg['To'] = 'kay.mckeon@realnation.ie'
```

Change to your desired email or add multiple recipients:

```python
msg['To'] = 'kay.mckeon@realnation.ie, stephen.maguire@realnation.ie'
```

### Change Schedule Time

Edit `email_scheduler.py`, line 40:

```python
schedule.every().friday.at("16:00").do(send_weekly_report)
```

Options:
- Daily: `schedule.every().day.at("09:00")`
- Monday: `schedule.every().monday.at("16:00")`
- Multiple times: Add multiple `schedule.every()...` lines

### Customize Email Content

Edit the email HTML in `send_weekly_email_alert()` method to add:
- Company logo
- Additional statistics
- Different styling
- Attachments (Excel/PDF reports)

---

## ✅ Success Checklist

- [ ] SMTP settings configured in secrets
- [ ] Gmail App Password generated and added
- [ ] Manual email test successful from dashboard
- [ ] Email received in Kay's inbox
- [ ] Scheduler running (if automated)
- [ ] Scheduler log file being updated
- [ ] Weekly email arriving every Friday at 4 PM

---

## 🆘 Need Help?

1. Check the terminal output for detailed error messages
2. Review the `email_scheduler.log` file
3. Test with a personal email address first
4. Verify Google Sheets connection is working
5. Ensure you have admin privileges in the app

---

**Last Updated:** December 3, 2025
**Version:** 2.0 (with AIBFS support)

