# Fix Google Sheets Connection in Streamlit Cloud

## Problem
The app is showing: **"⚠️ Using demo mode - Google Sheets not connected. Only showing fallback users."**

This means the Google Sheets credentials are not being loaded from Streamlit Cloud secrets.

## Solution: Add/Update Secrets in Streamlit Cloud

### Step 1: Access Streamlit Cloud Settings

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Log in to your account
3. Find your app: **rn-time-tracker**
4. Click the **⋮** (three dots) menu next to your app
5. Click **Settings**
6. Scroll down to the **Secrets** section

### Step 2: Add/Update Secrets

Copy and paste the following into the Secrets field. **Make sure to use the exact format shown below:**

```toml
# Google Sheets Service Account Credentials (Nested Structure)
[GOOGLE_SHEETS_CREDENTIALS]
type = "service_account"
project_id = "rn-copy-checker-app"
private_key_id = "ff61d89a77d61765ea4e23df25e63f4d3628de0c"
private_key = """-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCvu7YDypiTB1ku
169oexuO5Jz17FYRBF167U3AZg6Iz3WkjA0SC0nt1kexjfOFaDBA1rgH0zveGbzf
y/s0YAWg+zphSTwE1FtaOZ6pOQ3G2ftlScFYoo1EdQ0XdoNauUTqSRTkI4pnVUEp
EjWbCU5pP27dly33KdmUSPIG7Y2IwoIubM3i92fgLPEYTW486qiOQ4lQ0fBgchYB
Ly0E9ljB7MmZgtqMVLvpAolQAGzfWVuPo3LdX3k79at5CnqW0iMGDUwBtImrDOEY
FOYZUHGqDoT0YciNR7vOX5AY5yeTqB7tHZt06aiG9glCj/uraSMnGwRHwEYOKVB5
3EGtPNvZAgMBAAECggEAMq+S/4PzPtELRYn7M0jyuWOx6/KHHnBiX/7LArfM8GPZ
/CRS7sXnxFweIJWfS/axmDn2KXehGF3XDrugUEpzxStA+udrEr+HO75Lx2ZH1Xdw
3ZWI2T5FPZ3/MSnDGCtAt8xtZKHlnQlHeoegg3+LKKsdmHcu0E+3TGA/woTI4k0w
1HpdFEV5CLpTs/WnruO9ehBBWZ1w+6o10yVbZN4Km6+7d2xSRFyfuquCmNjuIEVW
kcSSDR0f0l/xkzJUmmirLKykJ/DZvf10aeOVlx1hqraYubANXmhhKk7tfjeI31iG
VAVIMh6POTPnmW3qAD+DbetD2o95eQlbQ4HFkDW2iwKBgQDqcP3oa6ysvZhmiEP9
s+9W3LAxpubPmpHN4zo1k/2c6tVUxFrse9OIS0QtGm+j5V6IUQaPtiBUy8Pkw8X8
ge5QD/Y3+wYU8aCVxgefHNj9JjCHMKc6C3XGH1Po0NSQQbmQP7qstqAeoiS1BWp+
PJjpkLdiZz2H/S/1bjTJTDxwMwKBgQC/5KpITWN72hJpm7MQ5jiFxtCc6ybreqXb
R3iXm1C0La6fkOhxlius2cwvJW9ttokEZ6dPrdmW8+DC9iQDC5o3OvkoKCx1kO7a
D52l3Do6t+II5Kl4nzLfrG4whrPjoXcxMCayRH8qPdXVuH9ghBbq/046/CsQPUom
c9IysVYHwwKBgGppfSZo8Ui7ChjIEyxt5t4jb6op2qwyuamdUQeOs9fs04YVVjvu
/JXpq/lY/YGEFAOF25eRkF1M3A7TOeOiSjx28kh4nUsWXdB9wWncWzWUhwRl9hGn
r/6Mq7aKS2FrI8Iw2xeYEVe2OzkbSzofYTzq3gJBYDGAn6skKbuQ6gH3AoGBALKj
WupoMN7RiiaKbc6jo6bWCMqsFtVMni5egKMSUbUKee/N5LYpSItnTi/tt6f5L+DL
5fPFMjTW4DxfC/NRz8Tuv5hknc7sl46kzuvi8spK+L+yrxm9ioyzZvkBzWFxpRZD
byKxpXhbjD+ju+DL1tH5zogWzLgXdnoJhHrwn9glAoGBAOmPoWE8Qlr9nmDmRXDr
uy7I/zHbf2YSdLVMt20xhmzLWStkHvZLZNP4y/lNEjoWmKFIM6OL0eNCg0Fr4lT4
4/i8y+me7rsag/QgCqHGTSNpRg5/H7YYUDCVcjctwMJGVJ7vcg2yEUkH92mPMvh1
XrIU9qCV08zA5efeCAVXtVbs
-----END PRIVATE KEY-----"""
client_email = "rn-copy-checker@rn-copy-checker-app.iam.gserviceaccount.com"
client_id = "115437915658597519594"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/rn-copy-checker%40rn-copy-checker-app.iam.gserviceaccount.com"
universe_domain = "googleapis.com"

# Google Sheets Configuration (at root level, NOT inside GOOGLE_SHEETS_CREDENTIALS)
SPREADSHEET_ID = "1nLOJvUut6RgfYbsSQa1ghPnJMaUWdHbbvlWqSDwwmU4"
USERS_TAB_NAME = "Users"
TIME_ENTRIES_TAB_NAME = "Time Entries"
PROJECTS_TAB_NAME = "Projects"

# Gmail SMTP Settings (for weekly email alerts)
[GMAIL_SMTP_SETTINGS]
EMAIL_ADDRESS = "stephen.maguire@realnation.ie"
EMAIL_PASSWORD = "kfve rbuj jlvf nefw"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

### Step 3: Important Formatting Notes

⚠️ **CRITICAL**: Pay attention to these formatting requirements:

1. **Private Key**: Must use triple quotes `"""` and include the full key with `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----`
2. **Section Headers**: Use square brackets `[GOOGLE_SHEETS_CREDENTIALS]` and `[GMAIL_SMTP_SETTINGS]`
3. **SPREADSHEET_ID**: Must be at the **root level** (not inside the `[GOOGLE_SHEETS_CREDENTIALS]` section)
4. **No extra spaces**: Make sure there are no trailing spaces or extra characters

### Step 4: Save and Restart

1. Click **Save** at the bottom of the Secrets section
2. The app will automatically restart (takes about 30-60 seconds)
3. Wait for the app to finish restarting

### Step 5: Verify Connection

1. Open your app URL (e.g., `https://rn-time-tracker.streamlit.app`)
2. Check the login page - you should see:
   - ✅ **"Connected to Google Sheets - X users loaded"** (instead of the demo mode warning)
   - Users from your Google Sheet should appear in the dropdown
3. Check the app logs:
   - Go to Streamlit Cloud → Your App → ⋮ → **Manage app** → **Logs**
   - Look for messages like:
     - `✅ Credentials loaded from Streamlit secrets (nested)`
     - `✅ Successfully connected to Google Sheets!`
     - `📊 Spreadsheet: [Your Sheet Name]`

## Troubleshooting

### Problem: Still showing "demo mode" after adding secrets

**Check 1: Verify secrets are saved**
- Go back to Settings → Secrets
- Make sure the secrets are still there (sometimes they don't save if there's a syntax error)

**Check 2: Check app logs for errors**
- Go to **Manage app** → **Logs**
- Look for error messages like:
  - `❌ Credential validation failed`
  - `Missing or empty required field: [field name]`
  - `Private key format appears incorrect`

**Check 3: Verify TOML syntax**
- Make sure all section headers use `[SECTION_NAME]` format
- Make sure the private key uses triple quotes `"""`
- Make sure `SPREADSHEET_ID` is at root level (not inside `[GOOGLE_SHEETS_CREDENTIALS]`)

**Check 4: Verify Google Sheet is shared**
- Open your Google Sheet: https://docs.google.com/spreadsheets/d/1nLOJvUut6RgfYbsSQa1ghPnJMaUWdHbbvlWqSDwwmU4
- Click **Share** button
- Make sure this email has **Editor** access:
  - `rn-copy-checker@rn-copy-checker-app.iam.gserviceaccount.com`

### Problem: "Spreadsheet not found" error

1. **Verify Spreadsheet ID**: Make sure `SPREADSHEET_ID = "1nLOJvUut6RgfYbsSQa1ghPnJMaUWdHbbvlWqSDwwmU4"` matches your actual sheet
2. **Check sharing**: The sheet must be shared with the service account email
3. **Check tabs**: Make sure the sheet has these tabs:
   - `Users` (with columns: Name, Email, Password, Role)
   - `Time Entries` (for storing time entries)
   - `Projects` (optional, for project data)

### Problem: "Credential validation failed"

The app now validates credentials and will show specific errors:
- `Missing or empty required field: project_id` → Add `project_id` to secrets
- `Missing or empty required field: private_key` → Add `private_key` to secrets
- `Missing or empty required field: client_email` → Add `client_email` to secrets
- `Missing or empty required field: client_id` → Add `client_id` to secrets
- `Private key format appears incorrect` → Make sure private key starts with `-----BEGIN PRIVATE KEY-----`
- `Missing or empty SPREADSHEET_ID` → Add `SPREADSHEET_ID` at root level

### Problem: App logs show "No Google Sheets credentials found"

This means the secrets structure doesn't match what the app expects. The app looks for:
- **Option 1 (Flat)**: `project_id` and `client_email` at root level
- **Option 2 (Nested)**: `[GOOGLE_SHEETS_CREDENTIALS]` section

Use the nested structure shown in Step 2 above.

## Alternative: Flat Structure Format

If you prefer the flat structure (all keys at root level), use this format instead:

```toml
# Google Sheets Service Account Credentials (Flat Structure)
type = "service_account"
project_id = "rn-copy-checker-app"
private_key_id = "ff61d89a77d61765ea4e23df25e63f4d3628de0c"
private_key = """-----BEGIN PRIVATE KEY-----
[Same private key as above]
-----END PRIVATE KEY-----"""
client_email = "rn-copy-checker@rn-copy-checker-app.iam.gserviceaccount.com"
client_id = "115437915658597519594"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/rn-copy-checker%40rn-copy-checker-app.iam.gserviceaccount.com"
universe_domain = "googleapis.com"

# Google Sheets Configuration
SPREADSHEET_ID = "1nLOJvUut6RgfYbsSQa1ghPnJMaUWdHbbvlWqSDwwmU4"
USERS_TAB_NAME = "Users"
TIME_ENTRIES_TAB_NAME = "Time Entries"
PROJECTS_TAB_NAME = "Projects"

# Gmail SMTP Settings
EMAIL_ADDRESS = "stephen.maguire@realnation.ie"
EMAIL_PASSWORD = "kfve rbuj jlvf nefw"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

## Need More Help?

1. Check the app logs in Streamlit Cloud for detailed error messages
2. Review the improved error messages - they now show exactly what's missing
3. Contact Stephen Maguire (stephen.maguire@realnation.ie) for technical assistance

---

**Last Updated**: January 2026  
**App Version**: With improved credential validation and error messages

