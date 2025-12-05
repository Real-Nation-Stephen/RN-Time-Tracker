#!/usr/bin/env python3
"""
Weekly Email Scheduler for RN Time Tracker
Runs every Friday at 4PM to send weekly reports to Kay
"""

import schedule
import time
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rn_time_tracker import TimeTrackerApp

def send_weekly_report():
    """Send weekly email report"""
    print(f"[{datetime.now()}] Starting weekly email report...")
    
    try:
        app = TimeTrackerApp()
        success = app.send_weekly_email_alert()
        
        if success:
            print(f"[{datetime.now()}] ✅ Weekly email report sent successfully!")
        else:
            print(f"[{datetime.now()}] ❌ Failed to send weekly email report")
            
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error sending weekly report: {str(e)}")

def main():
    """Main scheduler function"""
    print("🕐 RN Time Tracker Email Scheduler Started")
    print("📧 Will send weekly reports every Friday at 4:00 PM")
    
    # Schedule the weekly email
    schedule.every().friday.at("16:00").do(send_weekly_report)
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
