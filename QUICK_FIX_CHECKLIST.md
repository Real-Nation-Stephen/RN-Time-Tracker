# Quick Fix Checklist for Google Sheets Connection

## ⚡ Quick Steps to Diagnose

### Step 1: Check App Logs (Most Important!)

1. Go to Streamlit Cloud → Your App
2. Click **⋮** → **Manage app** → **Logs**
3. Look for these messages:

**✅ Good signs:**
- `✅ Credentials loaded from Streamlit secrets`
- `✅ Successfully connected to Google Sheets!`
- `✅ Loaded X users from sheet`

**❌ Bad signs:**
- `⚠️ No Google Sheets credentials found`
- `❌ Credential validation failed`
- `❌ Spreadsheet with ID '...' not found`
- `PERMISSION_DENIED` errors

### Step 2: Use the Diagnostic Tool in the App

1. Open your app
2. If you see "⚠️ Using demo mode" warning
3. Click **"🔧 Diagnostic Information"** to expand
4. Click **"🔄 Test Connection"** button
5. This will show you exactly what's wrong

### Step 3: Verify Secrets Format

Go to Streamlit Cloud → Settings → Secrets and check:

```toml
# Must have this section:
[GOOGLE_SHEETS_CREDENTIALS]
type = "service_account"
project_id = "rn-copy-checker-app"
private_key = """-----BEGIN PRIVATE KEY-----
[full key here]
-----END PRIVATE KEY-----"""
client_email = "rn-copy-checker@rn-copy-checker-app.iam.gserviceaccount.com"
# ... other fields

# Must be at ROOT level (NOT inside [GOOGLE_SHEETS_CREDENTIALS]):
SPREADSHEET_ID = "1nLOJvUut6RgfYbsSQa1ghPnJMaUWdHbbvlWqSDwwmU4"
```

**Common mistakes:**
- ❌ `SPREADSHEET_ID` inside `[GOOGLE_SHEETS_CREDENTIALS]` section
- ❌ Private key not using triple quotes `"""`
- ❌ Missing `-----BEGIN PRIVATE KEY-----` or `-----END PRIVATE KEY-----`
- ❌ Extra spaces or formatting issues

### Step 4: Verify Google Sheet Sharing

1. Open your Google Sheet: https://docs.google.com/spreadsheets/d/1nLOJvUut6RgfYbsSQa1ghPnJMaUWdHbbvlWqSDwwmU4
2. Click **Share** button (top right)
3. Check if this email is in the list:
   - `rn-copy-checker@rn-copy-checker-app.iam.gserviceaccount.com`
4. If NOT, add it with **Editor** permissions
5. If YES, make sure it has **Editor** (not Viewer)

### Step 5: Verify Users Tab Structure

Your "Users" tab should have these columns in row 1:
- `Name`
- `Email`
- `Password`
- (Optional: `Profile Image`, `Role`, etc.)

**Important:**
- Column names must match exactly (case-sensitive)
- First row should be headers
- Data starts in row 2

If you added extra columns, that's fine - the app will just ignore them.

## 🔍 Most Common Issues

### Issue 1: "No Google Sheets credentials found"

**Cause:** Secrets not configured or wrong format

**Fix:**
1. Go to Streamlit Cloud → Settings → Secrets
2. Make sure you have `[GOOGLE_SHEETS_CREDENTIALS]` section
3. Make sure `SPREADSHEET_ID` is at root level
4. Click Save
5. Reboot app

### Issue 2: "Credential validation failed"

**Cause:** Missing required fields in secrets

**Fix:**
Check logs for which field is missing:
- `Missing or empty required field: project_id` → Add `project_id` to secrets
- `Missing or empty required field: private_key` → Add `private_key` to secrets
- `Missing or empty required field: client_email` → Add `client_email` to secrets
- `Missing or empty SPREADSHEET_ID` → Add `SPREADSHEET_ID` at root level

### Issue 3: "Spreadsheet not found" or "PERMISSION_DENIED"

**Cause:** Sheet not shared with service account

**Fix:**
1. Open Google Sheet
2. Click Share
3. Add: `rn-copy-checker@rn-copy-checker-app.iam.gserviceaccount.com`
4. Give it **Editor** permissions
5. Click Send

### Issue 4: "Users tab not found"

**Cause:** Tab name doesn't match or tab doesn't exist

**Fix:**
1. Check your sheet has a tab named exactly "Users" (case-sensitive)
2. Or update `USERS_TAB_NAME` in secrets to match your tab name

### Issue 5: Still showing demo users after fixing

**Cause:** App might be using cached connection

**Fix:**
1. Use the "🔄 Test Connection" button in the diagnostic section
2. Or reboot the app: Settings → Reboot app

## 📋 Verification Checklist

After making changes, verify:

- [ ] Secrets saved in Streamlit Cloud
- [ ] App rebooted (wait 30-60 seconds)
- [ ] Google Sheet shared with service account
- [ ] Service account has Editor permissions
- [ ] Users tab exists with correct column names
- [ ] Check app logs for ✅ success messages
- [ ] Test connection using diagnostic tool

## 🆘 Still Not Working?

1. **Check the logs** - They will tell you exactly what's wrong
2. **Use the diagnostic tool** in the app (expand "🔧 Diagnostic Information")
3. **Verify each step** in this checklist
4. **Check for typos** in secrets (especially spreadsheet ID)

---

**Need more help?** Check `GOOGLE_SHEETS_FIX_GUIDE.md` for detailed instructions.

