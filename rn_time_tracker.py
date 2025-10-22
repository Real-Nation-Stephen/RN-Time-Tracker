import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import gspread
from google.oauth2.service_account import Credentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import icalendar
import io
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import openpyxl
from openpyxl import Workbook
import re
import os
import json
import schedule
import time
import threading
from typing import Dict, List, Optional, Tuple
import requests
from PIL import Image

# Page configuration
try:
    favicon = Image.open("Icon.png")
    st.set_page_config(
        page_title="RN Time Tracker",
        page_icon=favicon,
        layout="wide",
        initial_sidebar_state="expanded"
    )
except:
    # Fallback if icon file not found
    st.set_page_config(
        page_title="RN Time Tracker",
        page_icon="⏰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Custom CSS - Light, clean styling matching quote app
st.markdown("""
<style>
    /* Overall app styling - light and clean */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #ffffff;
    }
    
    /* Main header styling */
    .main-header {
        text-align: center;
        color: #1f4e79;
        margin-bottom: 2rem;
        font-size: 2.5rem;
        font-weight: 600;
    }
    
    /* Section headers */
    h2, h3 {
        color: #1f4e79 !important;
        font-weight: 600;
    }
    
    /* Metric cards - clean and minimal with good contrast */
    .stMetric {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e9ecef;
    }
    
    .stMetric label {
        color: #495057 !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #1f4e79 !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Success and error boxes */
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #155724;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #721c24;
    }
    
    /* Balloon animation for week completion */
    .balloon-animation {
        animation: balloon 2s ease-in-out;
    }
    @keyframes balloon {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    /* Button styling - clean and professional with good contrast */
    .stButton>button {
        border-radius: 0.375rem;
        font-weight: 500;
        transition: all 0.2s ease;
        border: 1px solid #dee2e6;
        color: #212529 !important;
        background-color: #ffffff;
    }
    
    .stButton>button:hover {
        background-color: #f8f9fa;
        border-color: #adb5bd;
    }
    
    .stButton>button[kind="primary"],
    .stButton>button[kind="primary"] *,
    .stButton>button[kind="primary"] p,
    .stButton>button[kind="primary"] span,
    .stButton>button[kind="primary"] div,
    .stDownloadButton>button,
    .stDownloadButton>button * {
        background-color: #1f4e79 !important;
        border-color: #1f4e79 !important;
        color: #ffffff !important;
    }
    
    .stButton>button[kind="primary"]:hover,
    .stButton>button[kind="primary"]:hover *,
    .stButton>button[kind="primary"]:hover p,
    .stButton>button[kind="primary"]:hover span,
    .stButton>button[kind="primary"]:hover div,
    .stDownloadButton>button:hover,
    .stDownloadButton>button:hover * {
        background-color: #163a5f !important;
        border-color: #163a5f !important;
        color: #ffffff !important;
    }
    
    /* Sidebar styling - light and clean */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }
    
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #212529 !important;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] strong,
    section[data-testid="stSidebar"] * {
        color: #212529 !important;
    }
    
    /* Input fields - clean borders with good contrast */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stDateInput>div>div>input {
        border-radius: 0.375rem;
        border: 1px solid #ced4da;
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* ========================================
       DROPDOWN FIXES - MAXIMUM SPECIFICITY
       ======================================== */
    
    /* Kill all blue backgrounds in selectboxes */
    .stSelectbox select,
    .stSelectbox option,
    .stSelectbox > div,
    .stSelectbox div[data-baseweb="select"],
    .stSelectbox div[data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] > div > div {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* Navigation selectbox in sidebar */
    section[data-testid="stSidebar"] .stSelectbox select,
    section[data-testid="stSidebar"] .stSelectbox div,
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* All baseweb select components */
    div[data-baseweb="select"],
    div[data-baseweb="select"] *,
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div > div,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] svg {
        background-color: #ffffff !important;
        color: #212529 !important;
        fill: #212529 !important;
    }
    
    /* Popover dropdowns */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* All listbox elements */
    ul[role="listbox"],
    ul[role="listbox"] *,
    ul[role="listbox"] li,
    div[role="listbox"],
    div[role="listbox"] *,
    div[role="option"],
    div[role="option"] *,
    li[role="option"],
    li[role="option"] * {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* Hover states */
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li:hover *,
    div[role="option"]:hover,
    div[role="option"]:hover *,
    li[role="option"]:hover,
    li[role="option"]:hover * {
        background-color: #e9ecef !important;
        color: #212529 !important;
    }
    
    /* Selected/active states */
    ul[role="listbox"] li[aria-selected="true"],
    ul[role="listbox"] li[aria-selected="true"] *,
    div[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] *,
    li[role="option"][aria-selected="true"],
    li[role="option"][aria-selected="true"] * {
        background-color: #d4e7f7 !important;
        color: #212529 !important;
    }
    
    /* Dropdown backgrounds - but NOT plotly elements */
    div[class*="dropdown"]:not([class*="plot"]),
    div[class*="Dropdown"]:not([class*="plot"]),
    div[class*="select"]:not([class*="plot"]),
    div[class*="Select"]:not([class*="plot"]) {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* Button-like select triggers */
    div[data-baseweb="select"] [role="button"],
    div[data-baseweb="select"] [role="button"] *,
    div[data-baseweb="select"] [role="button"] > div,
    div[data-baseweb="select"] button,
    div[data-baseweb="select"] button * {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* Date input dropdowns */
    .stDateInput div,
    .stDateInput div *,
    .stDateInput select,
    .stDateInput option {
        background-color: #ffffff !important;
        color: #212529 !important;
    }
    
    /* Data editor and dataframe styling */
    .stDataFrame {
        border-radius: 0.5rem;
        border: 1px solid #e9ecef;
        overflow: hidden;
    }
    
    /* Don't override Plotly chart colors - remove aggressive selectors */
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed #ced4da;
        border-radius: 0.5rem;
        padding: 1rem;
        background-color: #f8f9fa;
    }
    
    /* Remove any dark backgrounds */
    div[data-testid="stHeader"] {
        background-color: #ffffff;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: #ffffff;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8f9fa;
        border-radius: 0.375rem;
        color: #495057;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1f4e79;
        color: #ffffff;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 0.375rem;
        font-weight: 500;
        color: #1f4e79 !important;
    }
    
    /* Info boxes - better contrast */
    .stAlert p, .stAlert div {
        color: #212529 !important;
    }
    
    /* General text contrast improvements */
    p, span, div, label {
        color: #212529;
    }
    
    /* Selectbox and input labels */
    label[data-testid="stWidgetLabel"] {
        color: #212529 !important;
        font-weight: 500;
    }
    
    /* Hamburger menu icon - make it visible */
    button[kind="header"] {
        color: #212529 !important;
    }
    
    button[kind="header"] svg {
        fill: #212529 !important;
    }
    
    /* Header elements */
    header[data-testid="stHeader"] {
        background-color: #ffffff !important;
    }
    
    header[data-testid="stHeader"] button {
        color: #212529 !important;
    }
    
    /* Radio buttons text */
    .stRadio label {
        color: #212529 !important;
    }
    
    .stRadio div[role="radiogroup"] label {
        color: #212529 !important;
    }
</style>
""", unsafe_allow_html=True)

class TimeTrackerApp:
    def __init__(self):
        self.authenticated = False
        self.user_role = None
        self.user_email = None
        self.user_name = None
        self.sheet_client = None
        self.worksheet = None
        self.load_credentials()
        
    def get_users_from_sheet(self) -> List[Dict]:
        """Get users from Google Sheets Users tab"""
        try:
            print("🔍 Loading users from Google Sheets...")
            
            if not self.connect_to_sheets():
                # Fallback to demo users if no connection
                print("⚠️  Using demo mode - Google Sheets not connected")
                return [
                    {"name": "Kay", "email": "kay@realnation.ie", "role": "admin", "password": ""},
                    {"name": "Stephen", "email": "stephen@realnation.ie", "role": "admin", "password": ""}
                ]
            
            # Get users from the Users tab
            try:
                print(f"🔍 Accessing '{self.users_tab}' worksheet...")
                users_sheet = self.spreadsheet.worksheet(self.users_tab)
                
                records = users_sheet.get_all_records()
                print(f"✅ Found {len(records)} records in Users sheet")
                
                users = []
                for record in records:
                    # Map columns from the sheet (Name, Email, Password, Profile Image)
                    name = str(record.get('Name', '')).strip()
                    email = str(record.get('Email', '')).strip()
                    password = str(record.get('Password', '')).strip()
                    
                    if name and email:
                            users.append({
                            "name": name,
                            "email": email,
                            "role": "admin",  # For now, all users from this sheet are admins
                            "password": password
                        })
                
                print(f"✅ Loaded {len(users)} users from sheet")
                return users if users else [
                    {"name": "Kay", "email": "kay@realnation.ie", "role": "admin", "password": ""},
                    {"name": "Stephen", "email": "stephen@realnation.ie", "role": "admin", "password": ""}
                ]
                    
            except gspread.WorksheetNotFound:
                print(f"⚠️  '{self.users_tab}' tab not found - using demo mode")
                print(f"📋 Please create a '{self.users_tab}' tab in your Google Sheet")
                return [
                    {"name": "Kay", "email": "kay@realnation.ie", "role": "admin", "password": ""},
                    {"name": "Stephen", "email": "stephen@realnation.ie", "role": "admin", "password": ""}
                ]
            except Exception as e:
                print(f"⚠️  Could not access users sheet: {str(e)}")
                return [
                    {"name": "Kay", "email": "kay@realnation.ie", "role": "admin", "password": ""},
                    {"name": "Stephen", "email": "stephen@realnation.ie", "role": "admin", "password": ""}
                ]
                
        except Exception as e:
            print(f"❌ Failed to load users: {str(e)}")
            return [
                {"name": "Kay", "email": "kay@realnation.ie", "role": "admin", "password": ""},
                {"name": "Stephen", "email": "stephen@realnation.ie", "role": "admin", "password": ""}
            ]
    
    def authenticate(self, user_name: str, password: str) -> bool:
        """Authenticate user via Google Sheets API"""
        try:
            # Get users from sheet
            users = self.get_users_from_sheet()
            
            # Find the selected user
            selected_user = None
            for user in users:
                if user["name"] == user_name:
                    selected_user = user
                    break
            
            if not selected_user:
                st.error("User not found")
                return False
                
            # Verify password against Google Sheets
            stored_password = selected_user.get("password", "")
            
            # If no password is stored in sheets, use demo mode
            if not stored_password:
                print("⚠️  No password stored - using demo mode")
                if password:  # Any non-empty password works in demo mode
                    self.user_role = selected_user["role"]
                    self.user_email = selected_user["email"]
                    self.user_name = selected_user["name"]
                    self.authenticated = True
                    return True
                else:
                    st.error("Password is required")
                    return False
            else:
                # Verify actual password
                if password == stored_password:
                    self.user_role = selected_user["role"]
                    self.user_email = selected_user["email"]
                    self.user_name = selected_user["name"]
                    self.authenticated = True
                    return True
                else:
                    st.error("Invalid password")
                    return False
            
        except Exception as e:
            st.error(f"Authentication failed: {str(e)}")
            return False
    
    def parse_ics_file(self, ics_content: str, is_meetings: bool = False) -> List[Dict]:
        """Parse ICS file and extract events"""
        try:
            calendar = icalendar.Calendar.from_ical(ics_content)
            events = []
            
            for component in calendar.walk():
                if component.name == "VEVENT":
                    # Get start and end times
                    start_dt = component.get('dtstart').dt if component.get('dtstart') else None
                    end_dt = component.get('dtend').dt if component.get('dtend') else None
                    
                    # Normalize to datetime objects (handle both date and datetime)
                    # Convert to local timezone for display
                    from datetime import timezone
                    import pytz
                    
                    # Assume Europe/Dublin (Ireland) timezone
                    local_tz = pytz.timezone('Europe/Dublin')
                    
                    if start_dt:
                        if isinstance(start_dt, datetime):
                            # If it has timezone info, convert to local
                            if start_dt.tzinfo is not None:
                                start_dt = start_dt.astimezone(local_tz)
                            else:
                                # If no timezone, assume it's already local
                                start_dt = local_tz.localize(start_dt)
                        else:
                            # Convert date to datetime at midnight in local timezone
                            start_dt = local_tz.localize(datetime.combine(start_dt, datetime.min.time()))
                    
                    if end_dt:
                        if isinstance(end_dt, datetime):
                            # If it has timezone info, convert to local
                            if end_dt.tzinfo is not None:
                                end_dt = end_dt.astimezone(local_tz)
                            else:
                                # If no timezone, assume it's already local
                                end_dt = local_tz.localize(end_dt)
                        else:
                            # Convert date to datetime at midnight in local timezone
                            end_dt = local_tz.localize(datetime.combine(end_dt, datetime.min.time()))
                    
                    event = {
                        'summary': str(component.get('summary', '')),
                        'start': start_dt,
                        'end': end_dt,
                        'description': str(component.get('description', '')),
                        'location': str(component.get('location', '')),
                        'is_meeting': is_meetings  # Tag if this is from meetings calendar
                    }
                    events.append(event)
            
            return events
        except Exception as e:
            st.error(f"Error parsing ICS file: {str(e)}")
            print(f"❌ ICS parsing error: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return []
    
    def get_projects_from_sheet(self) -> List[Dict]:
        """Get projects list from Google Sheets Projects tab"""
        try:
            if not self.connect_to_sheets():
                return []
            
            try:
                print(f"🔍 Loading projects from 'Projects' worksheet...")
                projects_sheet = self.spreadsheet.worksheet("Projects")
                records = projects_sheet.get_all_records()
                
                projects = []
                for record in records:
                    project_code = str(record.get('Project Code', '')).strip()
                    job_number = str(record.get('Job Number', '')).strip()
                    
                    if project_code or job_number:  # At least one identifier needed
                        client = str(record.get('Client', '')).strip()
                        project = str(record.get('Project', '')).strip()
                        job = str(record.get('Job', '')).strip()
                        
                        # Format: Client - Project - Code
                        # Example: "Design - Gen Admin - M510"
                        parts = []
                        if client:
                            parts.append(client)
                        if project:
                            parts.append(project)
                        if project_code:
                            parts.append(project_code)
                        
                        display_name = " - ".join(parts) if parts else f"{project_code} {job_number}"
                        
                        projects.append({
                            'project_code': project_code,
                            'job_number': job_number,
                            'client': client,
                            'project': project,
                            'job': job,
                            'version': str(record.get('Version', '')).strip(),
                            'display_name': display_name
                        })
                
                print(f"✅ Loaded {len(projects)} projects from sheet")
                return projects
                
            except gspread.WorksheetNotFound:
                print("⚠️  'Projects' tab not found")
                return []
            except Exception as e:
                print(f"⚠️  Error loading projects: {str(e)}")
                return []
                
        except Exception as e:
            print(f"❌ Failed to load projects: {str(e)}")
            return []
    
    def auto_tag_common_activities(self, title: str) -> Optional[Dict]:
        """Auto-tag common activities like meetings, admin, training, etc."""
        title_lower = title.lower()
        
        # Check for keywords and return matching project
        if 'meeting' in title_lower or 'catchup' in title_lower or 'catch up' in title_lower:
            return {
                'project_code': 'M510',
                'job_number': 'NA',
                'client': 'Design',
                'project': 'Team Meetings',
                'job': '',
                'version': 'NA',
                'parsed': True,
                'auto_tagged': True
            }
        
        if 'admin' in title_lower:
            return {
                'project_code': 'M510',
                'job_number': 'NA',
                'client': 'Design',
                'project': 'Gen Admin',
                'job': '',
                'version': 'NA',
                'parsed': True,
                'auto_tagged': True
            }
        
        if 'training' in title_lower:
            return {
                'project_code': 'M510',
                'job_number': 'NA',
                'client': 'Design',
                'project': 'Training',
                'job': '',
                'version': 'NA',
                'parsed': True,
                'auto_tagged': True
            }
        
        if 'mgmt' in title_lower or 'management' in title_lower:
            return {
                'project_code': 'M510',
                'job_number': 'NA',
                'client': 'Design',
                'project': 'Mgmt',
                'job': '',
                'version': 'NA',
                'parsed': True,
                'auto_tagged': True
            }
        
        return None
    
    def parse_event_title(self, title: str) -> Dict:
        """Parse event title to extract project information"""
        # First, check for auto-taggable common activities
        auto_tag = self.auto_tag_common_activities(title)
        if auto_tag:
            return auto_tag
        
        # Updated pattern to be more flexible:
        # - Project code can be 2-4 letters followed by digits, OR just digits
        # - Job number always starts with D followed by digits
        # Examples: EJ983 D2057, 983 D2057, EIRG123 D4567
        
        # Try pattern with project code (letters + digits or just digits) and D-number
        patterns = [
            # Pattern 1: Full format with underscores
            r'([A-Z]*\d+)\s+(D\d{4})\s+([^_]+)_([^_]+)_([^_]+)_(.+)',
            # Pattern 2: Simpler format with just code, D-number, and underscores
            r'([A-Z]*\d+)\s+(D\d{4})\s+(.+)',
            # Pattern 3: Just D-number with underscores
            r'(D\d{4})\s+([^_]+)_([^_]+)_([^_]+)_(.+)',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, title, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) == 6:
                    # Full pattern match
                    return {
                        'project_code': groups[0].upper() if groups[0] else '',
                        'job_number': groups[1].upper() if groups[1] else '',
                        'client': groups[2],
                        'project': groups[3],
                        'job': groups[4],
                        'version': groups[5],
                        'parsed': True
                    }
                elif len(groups) == 3:
                    # Simple pattern - just code and D-number
                    return {
                        'project_code': groups[0].upper() if groups[0] else '',
                        'job_number': groups[1].upper() if groups[1] else '',
                        'client': '',
                        'project': '',
                        'job': groups[2],  # Use remaining text as job description
                        'version': '',
                        'parsed': True
                    }
                elif len(groups) == 5:
                    # D-number first
                    return {
                        'project_code': '',
                        'job_number': groups[0].upper() if groups[0] else '',
                        'client': groups[1],
                        'project': groups[2],
                        'job': groups[3],
                        'version': groups[4],
                        'parsed': True
                    }
        
        # If no pattern matched, return empty with parsed=False flag
            return {
                'project_code': '',
                'job_number': '',
                'client': '',
                'project': '',
            'job': title,  # Keep full title as job description
            'version': '',
            'parsed': False
            }
    
    def check_overlaps(self, events: List[Dict]) -> List[Dict]:
        """Check for overlapping events and flag them"""
        overlaps = []
        sorted_events = sorted(events, key=lambda x: x['start'])
        
        for i in range(len(sorted_events) - 1):
            current = sorted_events[i]
            next_event = sorted_events[i + 1]
            
            if current['end'] and next_event['start']:
                if current['end'] > next_event['start']:
                    overlaps.append({
                        'event1': current,
                        'event2': next_event,
                        'overlap_duration': current['end'] - next_event['start']
                    })
        
        return overlaps
    
    def load_credentials(self):
        """Load Google Sheets API credentials from Streamlit secrets or local file"""
        # Initialize default values
        self.credentials = None
        self.smtp_settings = None
        self.spreadsheet_id = None
        self.users_tab = 'Users'
        self.time_entries_tab = 'Time Entries'
        
        try:
            # Try Streamlit secrets first (for cloud deployment)
            # Try FLAT structure first (like quote app), then nested structure
            try:
                if hasattr(st, 'secrets'):
                    # Try flat structure (individual keys at top level)
                    if 'project_id' in st.secrets and 'client_email' in st.secrets:
                        print("🔍 Debug: Loading credentials from Streamlit secrets (flat structure)...")
                        self.credentials = {
                            "type": st.secrets.get("type", "service_account"),
                            "project_id": st.secrets.get("project_id", ""),
                            "private_key_id": st.secrets.get("private_key_id", ""),
                            "private_key": st.secrets.get("private_key", ""),
                            "client_email": st.secrets.get("client_email", ""),
                            "client_id": st.secrets.get("client_id", ""),
                            "auth_uri": st.secrets.get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
                            "token_uri": st.secrets.get("token_uri", "https://oauth2.googleapis.com/token"),
                            "auth_provider_x509_cert_url": st.secrets.get("auth_provider_x509_cert_url", "https://www.googleapis.com/oauth2/v1/certs"),
                            "client_x509_cert_url": st.secrets.get("client_x509_cert_url", ""),
                            "universe_domain": st.secrets.get("universe_domain", "googleapis.com")
                        }
                        self.spreadsheet_id = st.secrets.get("SPREADSHEET_ID", "")
                        self.users_tab = st.secrets.get("USERS_TAB_NAME", "Users")
                        self.time_entries_tab = st.secrets.get("TIME_ENTRIES_TAB_NAME", "Time Entries")
                        self.smtp_settings = None
                        
                        print(f"✅ Credentials loaded from Streamlit secrets (flat)")
                        print(f"🔍 Project ID: {self.credentials.get('project_id', 'NOT SET')}")
                        print(f"🔍 Client Email: {self.credentials.get('client_email', 'NOT SET')}")
                        print(f"🔍 Spreadsheet ID: {self.spreadsheet_id}")
                        return
                    
                    # Try nested structure (keys under GOOGLE_SHEETS_CREDENTIALS section)
                    elif 'GOOGLE_SHEETS_CREDENTIALS' in st.secrets:
                        print("🔍 Debug: Loading credentials from Streamlit secrets (nested structure)...")
                        creds_section = st.secrets["GOOGLE_SHEETS_CREDENTIALS"]
                        
                        self.credentials = {
                            "type": creds_section.get("type", "service_account"),
                            "project_id": creds_section.get("project_id", ""),
                            "private_key_id": creds_section.get("private_key_id", ""),
                            "private_key": creds_section.get("private_key", ""),
                            "client_email": creds_section.get("client_email", ""),
                            "client_id": creds_section.get("client_id", ""),
                            "auth_uri": creds_section.get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
                            "token_uri": creds_section.get("token_uri", "https://oauth2.googleapis.com/token"),
                            "auth_provider_x509_cert_url": creds_section.get("auth_provider_x509_cert_url", "https://www.googleapis.com/oauth2/v1/certs"),
                            "client_x509_cert_url": creds_section.get("client_x509_cert_url", ""),
                            "universe_domain": creds_section.get("universe_domain", "googleapis.com")
                        }
                        self.spreadsheet_id = st.secrets.get("SPREADSHEET_ID", "")
                        self.users_tab = st.secrets.get("USERS_TAB_NAME", "Users")
                        self.time_entries_tab = st.secrets.get("TIME_ENTRIES_TAB_NAME", "Time Entries")
                        
                        if 'GMAIL_SMTP_SETTINGS' in st.secrets:
                            self.smtp_settings = dict(st.secrets['GMAIL_SMTP_SETTINGS'])
                        else:
                            self.smtp_settings = None
                        
                        print(f"✅ Credentials loaded from Streamlit secrets (nested)")
                        print(f"🔍 Project ID: {self.credentials.get('project_id', 'NOT SET')}")
                        print(f"🔍 Client Email: {self.credentials.get('client_email', 'NOT SET')}")
                        print(f"🔍 Spreadsheet ID: {self.spreadsheet_id}")
                        return
            except Exception as e:
                print(f"⚠️  Failed to load from Streamlit secrets: {str(e)}")
                print(f"🔍 Error type: {type(e).__name__}")
                # Continue to fallback
            
            # Fall back to local file (for local development)
            print("🔍 Debug: Loading credentials from auth/password_sheet_api.py...")
            from auth.password_sheet_api import (
                GOOGLE_SHEETS_CREDENTIALS, 
                GMAIL_SMTP_SETTINGS,
                SPREADSHEET_ID,
                USERS_TAB_NAME,
                TIME_ENTRIES_TAB_NAME
            )
            self.credentials = GOOGLE_SHEETS_CREDENTIALS
            self.smtp_settings = GMAIL_SMTP_SETTINGS
            self.spreadsheet_id = SPREADSHEET_ID
            self.users_tab = USERS_TAB_NAME
            self.time_entries_tab = TIME_ENTRIES_TAB_NAME
            
            print(f"✅ Credentials loaded from local file")
            print(f"🔍 Project ID: {self.credentials.get('project_id', 'NOT SET')}")
            print(f"🔍 Client Email: {self.credentials.get('client_email', 'NOT SET')}")
            print(f"🔍 Spreadsheet ID: {self.spreadsheet_id}")
                
        except ImportError as e:
            print("⚠️  Authentication credentials not found. Using demo mode.")
            print(f"🔍 Debug: Import error: {str(e)}")
            self.credentials = None
            self.smtp_settings = None
            self.spreadsheet_id = None
        except Exception as e:
            print(f"❌ Failed to load credentials: {str(e)}")
            self.credentials = None
            self.smtp_settings = None
            self.spreadsheet_id = None
    
    def connect_to_sheets(self):
        """Connect to Google Sheets"""
        try:
            if not self.credentials or not self.spreadsheet_id:
                print("⚠️  No Google Sheets credentials or spreadsheet ID found")
                return False
                
            print(f"🔍 Connecting to Google Sheets...")
            
            # Use your suggested pattern
            scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
            creds = Credentials.from_service_account_info(self.credentials, scopes=scopes)
            self.sheet_client = gspread.authorize(creds)
            self.spreadsheet = self.sheet_client.open_by_key(self.spreadsheet_id)
            
            print(f"✅ Successfully connected to Google Sheets!")
            print(f"📊 Spreadsheet: {self.spreadsheet.title}")
            return True
            
        except gspread.SpreadsheetNotFound:
            print(f"❌ Spreadsheet with ID '{self.spreadsheet_id}' not found.")
            print("📋 Make sure the spreadsheet is shared with your service account email.")
            return False
        except Exception as e:
            print(f"❌ Failed to connect to Google Sheets: {str(e)}")
            print(f"🔍 Error type: {type(e).__name__}")
            return False
    
    def save_time_entries(self, entries: List[Dict]) -> bool:
        """Save time entries to Google Sheets (checking for duplicates)"""
        try:
            if not self.connect_to_sheets():
                return False
            
            # Get the Time Entries worksheet
            try:
                time_entries_sheet = self.spreadsheet.worksheet(self.time_entries_tab)
            except gspread.WorksheetNotFound:
                # Create the worksheet if it doesn't exist
                print(f"⚠️  '{self.time_entries_tab}' tab not found, creating it...")
                time_entries_sheet = self.spreadsheet.add_worksheet(
                    title=self.time_entries_tab, 
                    rows=1000, 
                    cols=12
                )
                # Add header row
                headers = [
                    'Date', 'Start Time', 'End Time', 'Duration', 
                    'Project Code', 'Job Number', 'Client', 'Project', 
                    'Job', 'Version', 'User Email', 'Timestamp'
                ]
                time_entries_sheet.append_row(headers)
            
            # Get existing entries to check for duplicates
            existing_records = time_entries_sheet.get_all_records()
            existing_keys = set()
            for record in existing_records:
                # Create unique key: date + start_time + end_time + user_email
                key = f"{record.get('Date')}_{record.get('Start Time')}_{record.get('End Time')}_{record.get('User Email')}"
                existing_keys.add(key)
            
            # Prepare data for Google Sheets (filter out duplicates)
            data = []
            skipped = 0
            for entry in entries:
                entry_key = f"{entry.get('date')}_{entry.get('start_time')}_{entry.get('end_time')}_{entry.get('user_email', self.user_email)}"
                
                if entry_key in existing_keys:
                    skipped += 1
                    print(f"⚠️  Skipping duplicate: {entry.get('date')} {entry.get('start_time')}-{entry.get('end_time')}")
                    continue
                
                row = [
                    entry.get('date', ''),
                    entry.get('start_time', ''),
                    entry.get('end_time', ''),
                    entry.get('duration', ''),
                    entry.get('project_code', ''),
                    entry.get('job_number', ''),
                    entry.get('client', ''),
                    entry.get('project', ''),
                    entry.get('job', ''),
                    entry.get('version', ''),
                    entry.get('user_email', self.user_email),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ]
                data.append(row)
            
            # Append to worksheet
            if data:
                time_entries_sheet.append_rows(data)
                print(f"✅ Saved {len(data)} new entries to Google Sheets")
                if skipped > 0:
                    st.info(f"ℹ️ {skipped} duplicate entries were skipped (already in sheet)")
                return True
            elif skipped > 0:
                st.warning(f"⚠️ All {skipped} entries already exist - no new data saved")
                return True
            return False
            
        except Exception as e:
            st.error(f"Failed to save entries: {str(e)}")
            print(f"❌ Error saving entries: {str(e)}")
            return False
    
    def get_time_entries(self, start_date: datetime, end_date: datetime, user_filter: str = None) -> pd.DataFrame:
        """Retrieve time entries from Google Sheets"""
        try:
            if not self.connect_to_sheets():
                # Return sample data if no connection
                return self.get_sample_data(start_date, end_date)
            
            # Get the Time Entries worksheet
            try:
                time_entries_sheet = self.spreadsheet.worksheet(self.time_entries_tab)
                records = time_entries_sheet.get_all_records()
            except gspread.WorksheetNotFound:
                print(f"⚠️  '{self.time_entries_tab}' tab not found")
                return self.get_sample_data(start_date, end_date)
            
            # Convert to DataFrame
            df = pd.DataFrame(records)
            
            if df.empty:
                return self.get_sample_data(start_date, end_date)
            
            # Normalize column names
            df.columns = [col.lower().replace(' ', '_') for col in df.columns]
            
            # Convert date column
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
                df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
            
            # Remove duplicates based on date, start_time, end_time, user_email
            # This handles cases where "Mark Week Complete" was clicked multiple times
            if not df.empty:
                duplicate_cols = ['date', 'start_time', 'end_time', 'user_email']
                available_dup_cols = [col for col in duplicate_cols if col in df.columns]
                
                if len(available_dup_cols) >= 3:
                    before_dedup = len(df)
                    df = df.drop_duplicates(subset=available_dup_cols, keep='first')
                    after_dedup = len(df)
                    
                    if before_dedup > after_dedup:
                        removed = before_dedup - after_dedup
                        print(f"🧹 Removed {removed} duplicate entries from Google Sheets data")
                        print(f"   (This happens when 'Mark Week Complete' is clicked multiple times)")
            
            # Filter by user if specified
            if user_filter and 'user_email' in df.columns:
                df = df[df['user_email'] == user_filter]
            
            return df if not df.empty else self.get_sample_data(start_date, end_date)
            
        except Exception as e:
            print(f"❌ Failed to retrieve entries: {str(e)}")
            return self.get_sample_data(start_date, end_date)
    
    def get_sample_data(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Generate sample data for demonstration"""
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        sample_data = []
        
        for date in date_range:
            if date.weekday() < 5:  # Weekdays only
                sample_data.append({
                    'date': date,
                    'start_time': '09:00',
                    'end_time': '17:00',
                    'duration': '8:00:00',
                    'project_code': 'EJ983',
                    'job_number': 'D2057',
                    'client': 'Coillte',
                    'project': 'TY Programme Development',
                    'job': 'Brand Identity',
                    'version': 'v1',
                    'user_email': self.user_email or 'demo@realnation.ie'
                })
        
        return pd.DataFrame(sample_data)
    
    def send_weekly_email_alert(self):
        """Send weekly email alert to Kay"""
        try:
            if not self.smtp_settings:
                print("⚠️  Email settings not configured")
                return False
            
            # Get current week's data
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            
            # Get all users' data for the week
            all_entries = self.get_time_entries(week_start, week_end)
            
            # Normalize column names
            all_entries.columns = [col.lower().replace(' ', '_') for col in all_entries.columns]
            
            # Check if we have data
            if all_entries.empty or 'user_email' not in all_entries.columns:
                print("⚠️  No data available for email report")
                return False
            
            # Calculate summary
            user_summary = all_entries.groupby('user_email').agg({
                'duration': 'sum',
                'project_code': 'count'
            }).reset_index()
            
            # Create email content
            subject = f"Weekly Time Tracking Report - {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}"
            
            body = f"""
            <h2>Weekly Time Tracking Report</h2>
            <p><strong>Week:</strong> {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}</p>
            
            <h3>Summary by User:</h3>
            <table border="1" style="border-collapse: collapse;">
                <tr>
                    <th>User</th>
                    <th>Total Hours</th>
                    <th>Entries</th>
                    <th>Status</th>
                </tr>
            """
            
            for _, row in user_summary.iterrows():
                status = "✅ Completed" if row['duration'] > 0 else "❌ No entries"
                body += f"""
                <tr>
                    <td>{row['user_email']}</td>
                    <td>{row['duration']}</td>
                    <td>{row['project_code']}</td>
                    <td>{status}</td>
                </tr>
                """
            
            body += "</table>"
            
            # Send email
            msg = MIMEMultipart()
            msg['From'] = self.smtp_settings['email']
            msg['To'] = 'kay@realnation.ie'
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_settings['smtp_server'], self.smtp_settings['smtp_port'])
            server.starttls()
            server.login(self.smtp_settings['email'], self.smtp_settings['app_password'])
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            st.error(f"Failed to send email: {str(e)}")
            return False
    
    def export_to_excel(self, data: pd.DataFrame, filename: str = None) -> bytes:
        """Export data to Excel format"""
        try:
            if filename is None:
                filename = f"time_tracker_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            # Prepare data copy
            export_data = data.copy()
            
            # Convert date column to date only (remove time)
            if 'date' in export_data.columns:
                export_data['date'] = pd.to_datetime(export_data['date']).dt.date
            
            output = io.BytesIO()
            
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                export_data.to_excel(writer, sheet_name='Time Entries', index=False)
                
                # Add summary sheet
                if 'user_email' in data.columns and 'project_code' in data.columns:
                    summary_data = data.groupby(['user_email', 'project_code']).agg({
                        'duration': 'sum',
                        'date': 'count'
                    }).reset_index()
                    summary_data.columns = ['User Email', 'Project Code', 'Total Duration', 'Entry Count']
                    summary_data.to_excel(writer, sheet_name='Summary', index=False)
            
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            st.error(f"Failed to export to Excel: {str(e)}")
            print(f"❌ Excel export error: {str(e)}")
            return None
    
    def export_to_pdf(self, data: pd.DataFrame) -> bytes:
        """Export data to PDF format"""
        try:
            output = io.BytesIO()
            doc = SimpleDocTemplate(output, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph("RN Time Tracker Report", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Summary
            summary_text = f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
            summary_text += f"Total entries: {len(data)}<br/>"
            summary_text += f"Date range: {data['date'].min()} to {data['date'].max()}"
            
            summary = Paragraph(summary_text, styles['Normal'])
            story.append(summary)
            story.append(Spacer(1, 12))
            
            # Data table
            table_data = [['Date', 'User', 'Project', 'Client', 'Duration']]
            for _, row in data.iterrows():
                table_data.append([
                    str(row.get('date', '')),
                    str(row.get('user_email', '')),
                    str(row.get('project_code', '')),
                    str(row.get('client', '')),
                    str(row.get('duration', ''))
                ])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#4472C4'),
                ('TEXTCOLOR', (0, 0), (-1, 0), '#FFFFFF'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), '#F2F2F2'),
                ('GRID', (0, 0), (-1, -1), 1, '#CCCCCC')
            ]))
            
            story.append(table)
            doc.build(story)
            output.seek(0)
            return output.getvalue()
            
        except Exception as e:
            st.error(f"Failed to export to PDF: {str(e)}")
            return None

def main():
    # Initialize session state
    if 'authenticated_user' not in st.session_state:
        st.session_state.authenticated_user = None
    
    # DEBUG: Show credentials status in UI
    if 'show_debug' not in st.session_state:
        st.session_state.show_debug = False
    
    # Create app instance (used for utility functions)
    app = TimeTrackerApp()
    
    # Show debug info if credentials failed to load
    if not app.credentials and st.session_state.get('show_debug', False):
        st.error("⚠️ Failed to load Google Sheets credentials")
        st.info("Using demo mode with fallback users")
    
    # Authentication Check
    if not st.session_state.authenticated_user:
        st.markdown('<h1 class="main-header">🔐 Login Required</h1>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown("""
            <div style="background-color: #f8f9fa; padding: 2rem; border-radius: 0.5rem; border: 1px solid #e9ecef; text-align: center;">
                <h3 style="color: #1f4e79;">Welcome to RN Time Tracker</h3>
                <p style="color: #495057;">Please select your name and enter your password to access the application.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("")  # Add spacing
        
        # Get users for dropdown
        users = app.get_users_from_sheet()
        user_names = [user["name"] for user in users]
        user_lookup = {user["name"]: user for user in users}
        
        # Show connection status
        if len(users) == 2 and users[0]["name"] == "Kay" and users[1]["name"] == "Stephen":
            st.warning("⚠️ Using demo mode - Google Sheets not connected. Only showing fallback users.")
        else:
            st.success(f"✅ Connected to Google Sheets - {len(users)} users loaded")
        
        # User selection
        selected_user = st.selectbox("Select your name", options=user_names, key="login_user")
        
        # Password input
        if selected_user:
            password_input = st.text_input("Enter your password", type="password", key="password_input")
        else:
            password_input = ""
        
        # Login button
        if st.button("🚀 Login", type="primary", use_container_width=True):
            if selected_user and password_input:
                user_data = user_lookup[selected_user]
                stored_password = user_data.get("password", "")
                
                # Check password
                if not stored_password:
                    # Demo mode - any password works
                    st.session_state.authenticated_user = user_data
                    st.rerun()
                elif stored_password == password_input:
                    st.session_state.authenticated_user = user_data
                    st.rerun()
                else:
                    st.error("❌ Invalid password. Please try again.")
            elif not selected_user:
                st.error("Please select a user to continue.")
            elif not password_input:
                st.error("Please enter your password.")
        
        st.stop()
    
    # User is authenticated, show the main app
    authenticated_user = st.session_state.authenticated_user
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"**Welcome, {authenticated_user['name']}!**")
        st.markdown(f"📧 {authenticated_user['email']}")
        st.markdown(f"👤 Role: {authenticated_user.get('role', 'user')}")
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated_user = None
            st.rerun()
        
        st.divider()
        
        # Navigation
        page = st.selectbox(
            "Navigate",
            ["Time Tracker", "Dashboard"],
            key="navigation"
        )
    
    # Set user info on app instance for backward compatibility
    app.user_name = authenticated_user['name']
    app.user_email = authenticated_user['email']
    app.user_role = authenticated_user.get('role', 'user')
    app.authenticated = True
    
    # Main header
    st.markdown('<h1 class="main-header">⏰ RN Time Tracker</h1>', unsafe_allow_html=True)
    
    # Show selected page
    if page == "Time Tracker":
        show_time_tracker(app)
    elif page == "Dashboard":
        show_dashboard(app)

def show_time_tracker(app):
    """Time Tracker View"""
    st.markdown("## 📥 Time Tracker")
    
    # Date range filter at the top
    st.markdown("### 📅 Select Time Period")
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        date_filter = st.selectbox(
            "Filter by:",
            ["Past 7 Days", "Past 30 Days", "Custom Date Range"],
            key="date_filter_selector"
        )
    
    # Calculate date range based on selection
    today = datetime.now().date()
    if date_filter == "Past 7 Days":
        start_date = today - timedelta(days=7)
        end_date = today
        with col2:
            st.info(f"📅 Showing: {start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}")
    elif date_filter == "Past 30 Days":
        start_date = today - timedelta(days=30)
        end_date = today
        with col2:
            st.info(f"📅 Showing: {start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}")
    else:  # Custom Date Range
        with col2:
            start_date = st.date_input(
                "Start Date",
                value=today - timedelta(days=7),
                key="custom_start_date"
            )
        with col3:
            end_date = st.date_input(
                "End Date",
                value=today,
                key="custom_end_date"
            )
    
    st.markdown("---")
    
    # Get projects list from Google Sheets for dropdown
    available_projects = app.get_projects_from_sheet()
    project_options = ["-- Select from list or enter manually --"] + [p['display_name'] for p in available_projects]
    project_lookup = {p['display_name']: p for p in available_projects}
    
    # Two file uploaders side by side
    st.markdown("### 📁 Upload Calendars")
    col1, col2 = st.columns(2)
    
    with col1:
        time_tracking_file = st.file_uploader(
            "📅 Upload Time Tracking Calendar (.ics)",
        type=['ics'],
            help="Export your Time Tracking calendar as .ics file",
            key="time_tracking_upload"
        )
    
    with col2:
        meetings_file = st.file_uploader(
            "🤝 Upload Meetings Calendar (.ics) - Optional",
            type=['ics'],
            help="Export your Meetings calendar to track meeting time",
            key="meetings_upload"
        )
    
    all_events = []
    
    # Parse time tracking calendar
    if time_tracking_file:
        ics_content = time_tracking_file.read().decode('utf-8')
        events = app.parse_ics_file(ics_content, is_meetings=False)
        all_events.extend(events)
        st.success(f"✅ Loaded {len(events)} events from Time Tracking calendar")
    
    # Parse meetings calendar
    if meetings_file:
        ics_content = meetings_file.read().decode('utf-8')
        meetings = app.parse_ics_file(ics_content, is_meetings=True)
        all_events.extend(meetings)
        st.success(f"✅ Loaded {len(meetings)} events from Meetings calendar")
    
    if all_events:
        # Filter events by selected date range
        filtered_events = []
        for event in all_events:
            if event['start']:
                event_date = event['start'].date() if hasattr(event['start'], 'date') else event['start']
                # Debug logging
                print(f"🔍 Event: {event['summary'][:50]} | Event date: {event_date} | Filter range: {start_date} to {end_date}")
                if start_date <= event_date <= end_date:
                    filtered_events.append(event)
                    print(f"  ✅ INCLUDED")
                else:
                    print(f"  ❌ FILTERED OUT")
        
        # Show filtering info
        if len(filtered_events) < len(all_events):
            # Show date range of actual events in calendar
            all_dates = [e['start'].date() if hasattr(e['start'], 'date') else e['start'] for e in all_events if e['start']]
            if all_dates:
                earliest = min(all_dates)
                latest = max(all_dates)
                st.info(f"ℹ️ Showing {len(filtered_events)} events (filtered from {len(all_events)} total). Calendar contains events from {earliest.strftime('%b %d, %Y')} to {latest.strftime('%b %d, %Y')}")
            else:
                st.info(f"ℹ️ Showing {len(filtered_events)} events (filtered from {len(all_events)} total events in the calendar)")
        
        if not filtered_events:
            # Show what dates are actually in the calendar
            all_dates = [e['start'].date() if hasattr(e['start'], 'date') else e['start'] for e in all_events if e['start']]
            if all_dates:
                earliest = min(all_dates)
                latest = max(all_dates)
                st.warning(f"⚠️ No events found in the selected date range ({start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')})")
                st.info(f"📅 Your calendar contains events from {earliest.strftime('%b %d, %Y')} to {latest.strftime('%b %d, %Y')}. Please adjust your date filter above.")
            else:
                st.warning(f"⚠️ No events found in the selected date range ({start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')})")
                st.info("💡 Try adjusting your date range or uploading a different calendar file.")
            return
        
        # Sort events by date and time (handle None values properly)
        from datetime import timezone
        filtered_events.sort(key=lambda x: x['start'] if x['start'] else datetime.min.replace(tzinfo=timezone.utc))
        
        # Check for overlaps (only in filtered events)
        overlaps = app.check_overlaps(filtered_events)
        if overlaps:
            st.warning(f"⚠️ Found {len(overlaps)} overlapping events in selected date range")
            with st.expander("View Overlapping Events"):
                for overlap in overlaps:
                    st.error(f"⚠️ {overlap['event1']['summary']} & {overlap['event2']['summary']}")
            
        # View toggle
        view_mode = st.radio("View Mode", ["📋 List View (Grouped by Day)", "📅 Calendar View"], horizontal=True)
        
        if view_mode == "📋 List View (Grouped by Day)":
            st.markdown("### 📋 Event Preview & Editing")
            st.info(f"💡 Showing {len(filtered_events)} events from {start_date.strftime('%b %d')} to {end_date.strftime('%b %d, %Y')}. **Uncheck 'Include?' boxes** to exclude events before signing off.")
            
            # Initialize session state for edited events if not exists
            if 'edited_events' not in st.session_state:
                st.session_state.edited_events = {}
            
            # Group events by date
            events_by_date = {}
            for event in filtered_events:
                if event['start']:
                    date_str = event['start'].strftime('%Y-%m-%d')
                    if date_str not in events_by_date:
                        events_by_date[date_str] = []
                    events_by_date[date_str].append(event)
            
            # Display events grouped by day
            all_entries = []
            for date_str in sorted(events_by_date.keys()):
                day_events = events_by_date[date_str]
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                day_name = date_obj.strftime('%A')
                
                # Day header with visual separation
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #1f4e79 0%, #2c5f8f 100%); 
                            color: white; 
                            padding: 0.75rem 1rem; 
                            border-radius: 0.5rem; 
                            margin: 1.5rem 0 1rem 0;
                            font-weight: 600;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    📅 {day_name}, {date_obj.strftime('%B %d, %Y')} — {len(day_events)} events
                </div>
                """, unsafe_allow_html=True)
                
                # Create editable table for this day
                event_data = []
                for idx, event in enumerate(day_events):
                    parsed = app.parse_event_title(event['summary'])
                    event_key = f"{date_str}_{idx}"
                    
                    event_data.append({
                        '_key': event_key,
                        'Include': True,  # Checkbox column
                        'Type': '🤝 Meeting' if event.get('is_meeting') else '⏰ Work',
                        'Start': event['start'].strftime('%H:%M') if event['start'] else '',
                        'End': event['end'].strftime('%H:%M') if event['end'] else '',
                        'Duration': str(event['end'] - event['start']).split(',')[0] if event['start'] and event['end'] else '',
                        'Project Code': parsed['project_code'],
                        'Job Number': parsed['job_number'],
                        'Client': parsed['client'],
                        'Project': parsed['project'],
                        'Job': parsed['job'],
                        'Version': parsed['version'],
                        'Auto-Parsed': '✅' if parsed.get('parsed', False) else '⚠️ Manual',
                        'Original Title': event['summary']
                    })
                
                df_day = pd.DataFrame(event_data)
                
                # Show dropdown for manually selecting projects (for unparsed items)
                unparsed_count = len([e for e in event_data if e['Auto-Parsed'] == '⚠️ Manual'])
                if unparsed_count > 0:
                    if available_projects:
                        with st.expander(f"⚠️ {unparsed_count} event(s) need project assignment - Click to assign", expanded=True):
                            st.info("💡 Select a project from the dropdown for events that weren't auto-parsed, or manually edit the table below.")
                            for idx, row in enumerate(event_data):
                                if row['Auto-Parsed'] == '⚠️ Manual':
                                    st.markdown(f"**Event:** {row['Original Title']}")
                                    st.caption(f"🕐 {row['Start']} - {row['End']}")
                                    selected = st.selectbox(
                                        "Select project from your list",
                                        options=project_options,
                                        key=f"project_select_{row['_key']}",
                                        help="Choose from your Projects sheet or enter manually in the table below"
                                    )
                                    if selected != "-- Select from list or enter manually --":
                                        project = project_lookup[selected]
                                        # Update the dataframe
                                        df_day.loc[idx, 'Project Code'] = project['project_code']
                                        df_day.loc[idx, 'Job Number'] = project['job_number']
                                        df_day.loc[idx, 'Client'] = project['client']
                                        df_day.loc[idx, 'Project'] = project['project']
                                        df_day.loc[idx, 'Job'] = project['job']
                                        df_day.loc[idx, 'Version'] = project['version']
                                        st.success(f"✅ Assigned: {project['display_name']}")
                                    st.divider()
                    else:
                        st.warning(f"⚠️ {unparsed_count} event(s) need manual assignment. No projects found in Google Sheets 'Projects' tab.")
                        st.info("💡 Add projects to the 'Projects' tab in your Google Sheet, or manually edit the table below.")
                
                # Editable table for this day with checkbox to exclude
                edited_df_day = st.data_editor(
                    df_day.drop(columns=['_key', 'Auto-Parsed']),
                use_container_width=True,
                    num_rows="fixed",
                    key=f"event_editor_{date_str}",
                    hide_index=True,
                    column_config={
                        "Include": st.column_config.CheckboxColumn(
                            "Include?",
                            help="Uncheck to exclude this event from your timesheet",
                            default=True,
                            width="small"
                        ),
                        "Type": st.column_config.TextColumn("Type", width="small"),
                        "Start": st.column_config.TextColumn("Start", width="small"),
                        "End": st.column_config.TextColumn("End", width="small"),
                        "Duration": st.column_config.TextColumn("Duration", width="small"),
                        "Original Title": st.column_config.TextColumn("Original Title", width="large")
                    }
                )
                
                # Show exclusion info
                excluded_count = len(edited_df_day[edited_df_day['Include'] == False])
                if excluded_count > 0:
                    st.warning(f"🚫 {excluded_count} event(s) will be excluded from this day")
                
                # Collect entries for this day (only included ones)
                for _, row in edited_df_day.iterrows():
                    # Skip if user unchecked the Include box
                    if not row.get('Include', True):
                        continue
                    
                    entry = {
                        'date': date_str,
                        'start_time': row['Start'],
                        'end_time': row['End'],
                        'duration': row['Duration'],
                        'project_code': row['Project Code'],
                        'job_number': row['Job Number'],
                        'client': row['Client'],
                        'project': row['Project'],
                        'job': row['Job'],
                        'version': row['Version'],
                        'user_email': app.user_email,
                        'event_type': row['Type']
                    }
                    all_entries.append(entry)
            
            # Sign-off section
            st.markdown("---")
            st.markdown("### ✅ Weekly Sign-off")
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.info("📋 Review all entries above and make any necessary edits before signing off your week.")
            
            with col2:
                if st.button("✅ Mark Week Complete", type="primary", use_container_width=True):
                    # Save to Google Sheets
                    if app.save_time_entries(all_entries):
                        st.balloons()
                        st.success("🎉 Week marked complete! Your entries have been saved.")
                    else:
                        st.error("❌ Failed to save entries. Please try again.")
        
        else:  # Calendar View
            st.markdown("### 📅 Calendar View")
            st.info(f"🚧 Calendar view coming soon! Showing {len(filtered_events)} events from {start_date.strftime('%b %d')} to {end_date.strftime('%b %d, %Y')}.")
            
            # Show simple grouped summary
            events_by_date = {}
            for event in filtered_events:
                if event['start']:
                    date_str = event['start'].strftime('%Y-%m-%d')
                    if date_str not in events_by_date:
                        events_by_date[date_str] = []
                    events_by_date[date_str].append(event)
            
            for date_str in sorted(events_by_date.keys()):
                day_events = events_by_date[date_str]
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                st.markdown(f"**{date_obj.strftime('%A, %B %d')}** — {len(day_events)} events")
                for event in day_events:
                    event_type = "🤝" if event.get('is_meeting') else "⏰"
                    time_str = f"{event['start'].strftime('%H:%M')} - {event['end'].strftime('%H:%M')}" if event['start'] and event['end'] else ""
                    st.markdown(f"  {event_type} {time_str}: {event['summary']}")

def show_dashboard(app):
    """Dashboard View"""
    st.markdown("## 📊 Dashboard")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    # Get data from Google Sheets
    data = app.get_time_entries(
        datetime.combine(start_date, datetime.min.time()),
        datetime.combine(end_date, datetime.max.time())
    )
    
    # Normalize column names to handle both capitalized and lowercase versions
    data.columns = [col.lower().replace(' ', '_') for col in data.columns]
    
    # Admin filters
    if app.user_role == "admin":
        st.markdown("### 🔍 Admin Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'user_email' in data.columns and not data.empty:
                user_filter = st.selectbox("Filter by User", ["All"] + list(data['user_email'].unique()))
            else:
                user_filter = "All"
                st.info("No user data available")
        
        with col2:
            if 'project_code' in data.columns and 'project' in data.columns and not data.empty:
                # Create project labels as "Code + Name"
                unique_projects = data[['project_code', 'project']].drop_duplicates()
                project_options = ["All"] + [f"{row['project_code']} {row['project']}" for _, row in unique_projects.iterrows()]
                selected_project = st.selectbox("Filter by Project", project_options)
                project_filter = selected_project.split(' ')[0] if selected_project != "All" else "All"
            else:
                project_filter = "All"
                st.info("No project data available")
        
        with col3:
            if 'client' in data.columns and not data.empty:
                client_filter = st.selectbox("Filter by Client", ["All"] + list(data['client'].unique()))
            else:
                client_filter = "All"
                st.info("No client data available")
        
        # Apply filters
        if user_filter != "All" and 'user_email' in data.columns:
            data = data[data['user_email'] == user_filter]
        if project_filter != "All" and 'project_code' in data.columns:
            data = data[data['project_code'] == project_filter]
        if client_filter != "All" and 'client' in data.columns:
            data = data[data['client'] == client_filter]
    else:
        # Regular users only see their own data
        if 'user_email' in data.columns:
            data = data[data['user_email'] == app.user_email]
    
    if data.empty:
        st.warning("No data found for the selected date range.")
        return
    
    # Calculate metrics properly
    total_entries = len(data)
    
    # Count unique working days (unique dates in the data)
    working_days = data['date'].nunique() if 'date' in data.columns else 0
    
    # Count unique projects
    unique_projects = data['project_code'].nunique() if 'project_code' in data.columns else 0
    
    # Calculate total hours from duration if available
    # Duration format is like "1:30:00" so we need to parse it
    total_hours = 0
    if 'duration' in data.columns:
        print(f"\n🔍 DEBUG: Processing {len(data)} total entries")
        print(f"🔍 DEBUG: Sample durations: {data['duration'].head(10).tolist()}")
        
        # Check for duplicates
        if 'date' in data.columns and 'start_time' in data.columns and 'user_email' in data.columns:
            duplicates = data.duplicated(subset=['date', 'start_time', 'end_time', 'user_email'], keep=False)
            if duplicates.any():
                print(f"⚠️  WARNING: Found {duplicates.sum()} duplicate entries!")
                print(f"⚠️  Duplicate details:\n{data[duplicates][['date', 'start_time', 'end_time', 'user_email']]}")
        
        for idx, duration in enumerate(data['duration']):
            try:
                if pd.notna(duration) and ':' in str(duration):
                    # Handle timedelta objects or strings
                    duration_str = str(duration)
                    # Remove "0 days" prefix if present
                    if 'days' in duration_str or 'day' in duration_str:
                        duration_str = duration_str.split(',')[-1].strip()
                    
                    parts = duration_str.split(':')
                    hours = int(parts[0]) if len(parts) > 0 else 0
                    minutes = int(parts[1]) if len(parts) > 1 else 0
                    seconds = int(parts[2].split('.')[0]) if len(parts) > 2 else 0
                    duration_hours = hours + (minutes / 60) + (seconds / 3600)
                    total_hours += duration_hours
                    
                    if idx < 5:  # Log first 5 for debugging
                        print(f"🔍 Entry {idx}: Duration string='{duration_str}' -> {duration_hours:.2f}h")
            except Exception as e:
                print(f"❌ Error parsing duration '{duration}': {e}")
                pass
        
        print(f"🔍 DEBUG: Total calculated hours: {total_hours:.2f}h from {len(data)} entries")
    
    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Entries", total_entries)
    
    with col2:
        st.metric("Working Days", working_days)
    
    with col3:
        st.metric("Total Hours", f"{total_hours:.1f}h" if total_hours > 0 else "0h")
    
    with col4:
        st.metric("Projects", unique_projects)
    
    # Charts
    col1, col2 = st.columns(2)
    
    # Brand colors for charts
    brand_colors = ['#7CC242', '#F7941D', '#00B5E2', '#662D91', '#EC008C', '#FFF200']
    
    with col1:
        st.markdown("### 📊 Entries by Date")
        daily_counts = data.groupby('date').size().reset_index(name='count')
        fig = px.bar(
            daily_counts, 
            x='date', 
            y='count', 
            title="Entries by Date",
            color_discrete_sequence=[brand_colors[0]],
            template='plotly_white',
            labels={'date': 'Date', 'count': 'Number of Entries'}
        )
        fig.update_traces(marker_color=brand_colors[0])
        fig.update_layout(
            font=dict(color='#212529', size=12),
            title_font=dict(color='#1f4e79', size=16),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True, theme=None, config={'displayModeBar': False})
    
    with col2:
        st.markdown("### ⏱️ Duration by Project")
        # Calculate duration in hours per project
        if 'project' in data.columns and 'duration' in data.columns:
            project_duration = []
            for project_name in data['project'].unique():
                if pd.notna(project_name):
                    project_data = data[data['project'] == project_name]
                    total_duration = 0
                    for duration in project_data['duration']:
                        try:
                            if pd.notna(duration) and ':' in str(duration):
                                duration_str = str(duration)
                                if 'days' in duration_str or 'day' in duration_str:
                                    duration_str = duration_str.split(',')[-1].strip()
                                parts = duration_str.split(':')
                                hours = int(parts[0]) if len(parts) > 0 else 0
                                minutes = int(parts[1]) if len(parts) > 1 else 0
                                total_duration += hours + (minutes / 60)
                        except:
                            pass
                    if total_duration > 0:
                        project_duration.append({'Project': project_name, 'Hours': round(total_duration, 2)})
            
            if project_duration:
                df_duration = pd.DataFrame(project_duration)
                fig = px.pie(
                    df_duration, 
                    values='Hours', 
                    names='Project', 
                    title="Duration by Project (Hours)",
                    color_discrete_sequence=brand_colors,
                    template='plotly_white'
                )
                fig.update_traces(textfont_size=12, marker=dict(colors=brand_colors, line=dict(color='white', width=2)))
                fig.update_layout(
                    font=dict(color='#212529', size=12),
                    title_font=dict(color='#1f4e79', size=16),
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True, theme=None, config={'displayModeBar': False})
            else:
                st.info("No duration data available")
        else:
            st.info("No project duration data available")
    
    # Additional charts for admins
    if app.user_role == "admin":
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👥 Entries by User")
            if 'user_email' in data.columns:
                user_counts = data['user_email'].value_counts().reset_index()
                user_counts.columns = ['User', 'Count']
                fig = px.bar(
                    user_counts, 
                    x='User', 
                    y='Count', 
                    title="Entries by User",
                    color_discrete_sequence=[brand_colors[2]],
                    template='plotly_white',
                    labels={'User': 'User Email', 'Count': 'Number of Entries'}
                )
                fig.update_traces(marker_color=brand_colors[2])
                fig.update_layout(
                    font=dict(color='#212529', size=12),
                    title_font=dict(color='#1f4e79', size=16),
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True, theme=None, config={'displayModeBar': False})
            else:
                st.info("No user data available")
        
        with col2:
            st.markdown("### 🏢 Duration by Client")
            if 'client' in data.columns and 'duration' in data.columns:
                client_duration = []
                for client_name in data['client'].unique():
                    if pd.notna(client_name):
                        client_data = data[data['client'] == client_name]
                        total_duration = 0
                        for duration in client_data['duration']:
                            try:
                                if pd.notna(duration) and ':' in str(duration):
                                    duration_str = str(duration)
                                    if 'days' in duration_str or 'day' in duration_str:
                                        duration_str = duration_str.split(',')[-1].strip()
                                    parts = duration_str.split(':')
                                    hours = int(parts[0]) if len(parts) > 0 else 0
                                    minutes = int(parts[1]) if len(parts) > 1 else 0
                                    total_duration += hours + (minutes / 60)
                            except:
                                pass
                        if total_duration > 0:
                            client_duration.append({'Client': client_name, 'Hours': round(total_duration, 2)})
                
                if client_duration:
                    df_duration = pd.DataFrame(client_duration)
                    fig = px.pie(
                        df_duration, 
                        values='Hours', 
                        names='Client', 
                        title="Duration by Client (Hours)",
                        color_discrete_sequence=brand_colors,
                        template='plotly_white'
                    )
                    fig.update_traces(textfont_size=12, marker=dict(colors=brand_colors, line=dict(color='white', width=2)))
                    fig.update_layout(
                        font=dict(color='#212529', size=12),
                        title_font=dict(color='#1f4e79', size=16),
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig, use_container_width=True, theme=None, config={'displayModeBar': False})
                else:
                    st.info("No client duration data available")
            else:
                st.info("No client duration data available")
    
    # Duration by Job chart (for everyone)
    st.markdown("### 📋 Duration by Job")
    if 'job_number' in data.columns and 'job' in data.columns and 'duration' in data.columns:
        job_duration = []
        for idx, row in data[['job_number', 'job']].drop_duplicates().iterrows():
            job_number = row['job_number']
            job_name = row['job']
            if pd.notna(job_number) or pd.notna(job_name):
                # Filter data for this job
                job_data = data[(data['job_number'] == job_number) & (data['job'] == job_name)]
                total_duration = 0
                for duration in job_data['duration']:
                    try:
                        if pd.notna(duration) and ':' in str(duration):
                            duration_str = str(duration)
                            if 'days' in duration_str or 'day' in duration_str:
                                duration_str = duration_str.split(',')[-1].strip()
                            parts = duration_str.split(':')
                            hours = int(parts[0]) if len(parts) > 0 else 0
                            minutes = int(parts[1]) if len(parts) > 1 else 0
                            total_duration += hours + (minutes / 60)
                    except:
                        pass
                if total_duration > 0:
                    job_label = f"{job_number} {job_name}" if pd.notna(job_number) and job_number else job_name
                    job_duration.append({'Job': job_label, 'Hours': round(total_duration, 2)})
        
        if job_duration:
            df_job_duration = pd.DataFrame(job_duration)
            fig = px.bar(
                df_job_duration, 
                x='Job', 
                y='Hours', 
                title="Duration by Job (Hours)",
                color_discrete_sequence=[brand_colors[3]],
                template='plotly_white',
                labels={'Job': 'Job Number + Name', 'Hours': 'Total Hours'}
            )
            fig.update_traces(marker_color=brand_colors[3])
            fig.update_layout(
                font=dict(color='#212529', size=12),
                title_font=dict(color='#1f4e79', size=16),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True, theme=None, config={'displayModeBar': False})
        else:
            st.info("No job duration data available")
    else:
        st.info("No job duration data available")
    
    # Data table
    st.markdown("### 📋 Detailed View")
    # Only include columns that exist
    available_cols = ['date', 'user_email', 'project_code', 'client', 'project', 'job', 'duration']
    display_cols = [col for col in available_cols if col in data.columns]
    if display_cols:
        display_data = data[display_cols].copy()
        st.dataframe(display_data, use_container_width=True)
    else:
        st.warning("No data columns available to display")
    
    # Export options
    st.markdown("### 📤 Export Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export to Excel"):
            excel_data = app.export_to_excel(data)
            if excel_data:
                st.download_button(
                    label="Download Excel File",
                    data=excel_data,
                    file_name=f"time_tracker_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    
    with col2:
        if st.button("📄 Export to PDF"):
            pdf_data = app.export_to_pdf(data)
            if pdf_data:
                st.download_button(
                    label="Download PDF File",
                    data=pdf_data,
                    file_name=f"time_tracker_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )
    
    with col3:
        if app.user_role == "admin" and st.button("📧 Send Weekly Alert"):
            if app.send_weekly_email_alert():
                st.success("✅ Weekly email alert sent!")
            else:
                st.error("❌ Failed to send email alert")

if __name__ == "__main__":
    main()
