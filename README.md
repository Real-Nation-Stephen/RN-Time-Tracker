# ⏰ RN Time Tracker

A comprehensive time tracking application for Real Nation, built with Streamlit and Google Sheets integration.

## 🚀 Features

### 🔐 Authentication
- Password-based login via Google Sheets API
- Role-based access (Admin/User)
- Secure credential management

### 📥 Time Tracking
- **ICS File Upload**: Import calendar events from dedicated "Time Tracking" calendar
- **Event Parsing**: Automatic extraction of project codes, job numbers, clients, and project details
- **Overlap Detection**: Flags overlapping events to prevent double-booking
- **Editable Entries**: Review and edit entries before sign-off
- **Weekly Sign-off**: Lock entries with balloon animation confirmation

### 📊 Dashboard
- **Visual Analytics**: Bar charts, pie charts, timelines, and heatmaps
- **Admin Features**: View all users' data with filters
- **User Features**: Personal time tracking summary
- **Export Options**: Excel and PDF reports
- **Real-time Data**: Live updates from Google Sheets

### 📧 Email Alerts
- **Weekly Reports**: Automatic Friday 4PM emails to Kay
- **User Status**: Shows completed vs. incomplete users
- **Summary Statistics**: Total hours and entry counts per user

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Real-Nation-Stephen/RN-Time-Tracker.git
   cd RN-Time-Tracker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up authentication**:
   - Copy your Google Sheets API credentials to `auth/password_sheet_api.py`
   - Update the Gmail SMTP settings for email alerts

4. **Run the application**:
   ```bash
   streamlit run rn_time_tracker.py
   ```

## 📋 Usage

### For Users
1. **Login** with your email and password
2. **Upload ICS file** from your Time Tracking calendar
3. **Review and edit** parsed events
4. **Sign off** your weekly hours

### For Admins
1. **Access all users' data** in the Dashboard
2. **Filter by user, project, or client**
3. **Export reports** in Excel or PDF format
4. **Send weekly email alerts** manually

## 🔧 Configuration

### Google Sheets Setup
- Create a Google Sheets document named "RN Time Tracker"
- Set up the following columns: Date, Start Time, End Time, Duration, Project Code, Job Number, Client, Project, Job, Version, User Email, Timestamp
- Share the sheet with your service account email

### Email Configuration
- Update `auth/password_sheet_api.py` with your Gmail app password
- Configure SMTP settings for weekly alerts

### Weekly Email Scheduler
Run the email scheduler to send automatic weekly reports:
```bash
python email_scheduler.py
```

## 📁 Project Structure

```
RN-Time-Tracker/
├── rn_time_tracker.py          # Main application
├── email_scheduler.py          # Weekly email scheduler
├── auth/
│   └── password_sheet_api.py   # Authentication credentials
├── assets/
│   └── favicon.png            # App favicon
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🎯 Event Title Parsing

The application automatically parses event titles in the format:
```
EJ983 D2057 Coillte_TY Programme Development_Brand Identity_v1
```

**Extracted Information**:
- Project Code: EJ983
- Job Number: D2057
- Client: Coillte
- Project: TY Programme Development
- Job: Brand Identity
- Version: v1

## 🔒 Security

- Credentials stored securely in `auth/` directory
- Role-based access control
- Google Sheets API authentication
- Secure email transmission

## 📞 Support

For issues or questions, contact the development team or create an issue on GitHub.

## 📄 License

This project is proprietary to Real Nation. All rights reserved.
