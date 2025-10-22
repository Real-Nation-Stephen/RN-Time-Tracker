# Deploying RN Time Tracker to Streamlit Cloud

## Step 1: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Click "New app"
3. Connect your GitHub account if not already connected
4. Select:
   - **Repository:** `Real-Nation-Stephen/RN-Time-Tracker`
   - **Branch:** `main`
   - **Main file path:** `rn_time_tracker.py`
5. Click "Deploy"

## Step 2: Add Secrets to Streamlit Cloud

**IMPORTANT:** Before the app will work, you need to add your Google Sheets credentials as secrets.

1. In your Streamlit Cloud dashboard, click on your app
2. Click the "⋮" menu (three dots) → **Settings**
3. Go to the **Secrets** section
4. Copy and paste the following, **replacing with your actual credentials**:

```toml
# Google Sheets Service Account Credentials
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
5fPFMjTW4DxfC/NRz8Tuv5hknc7sl46kzuvi8spK+L+yrxm7ioyzZvkBzWFxpRZD
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

# Google Sheets Configuration
SPREADSHEET_ID = "1nLOJvUut6RgfYbsSQa1ghPnJMaUWdHbbvlWqSDwwmU4"
USERS_TAB_NAME = "Users"
TIME_ENTRIES_TAB_NAME = "Time Entries"
PROJECTS_TAB_NAME = "Projects"

# Gmail SMTP Settings (optional - for email alerts)
[GMAIL_SMTP_SETTINGS]
smtp_server = "smtp.gmail.com"
smtp_port = 587
email = "kay@realnation.ie"
app_password = "kfve rbuj jlvf nefw"
```

5. Click **Save**
6. The app will automatically restart with the secrets loaded

## Step 3: Verify Deployment

1. Wait for the app to finish deploying (usually takes 1-2 minutes)
2. Open the app URL provided by Streamlit Cloud
3. Log in with your credentials from the Google Sheet
4. Test uploading an ICS file

## Troubleshooting

- **"Failed to load credentials" error**: Make sure you've added the secrets correctly in Step 2
- **Login not working**: Verify the Google Sheet has a "Users" tab with Name, Email, and Password columns
- **Can't see time entries**: Make sure the Google Sheet has a "Time Entries" tab

## App URL

Once deployed, your app will be available at:
`https://rn-time-tracker.streamlit.app` (or similar)

You can customize the URL in your Streamlit Cloud settings.

