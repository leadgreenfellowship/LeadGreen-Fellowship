import csv
import smtplib
import json
import os
import time
from email.message import EmailMessage

# ==============================================================================
# ----------------------------- CONFIGURATION ----------------------------------
# ==============================================================================

# 1. Provide your Gmail Address
EMAIL_ADDRESS = "your.email@gmail.com"

# 2. Provide a 16-character App Password (NOT your normal Gmail password!)
# How to get this: Go to Google Account Settings -> Security -> 2-Step Verification -> App Passwords
EMAIL_APP_PASSWORD = "your-app-password-here"

# 3. Path to the CSV file you downloaded from your Admin Dashboard
CSV_FILE_PATH = "LeadGreen_Selected_Fellows.csv"  

# 4. Maximum emails to send today (Leave under 500 to be safe with Google)
MAX_EMAILS_PER_RUN = 400

# File that keeps track of who has already been emailed so we don't spam anyone twice.
TRACKING_FILE = "email_tracking.json"


# ==============================================================================
# ------------------------------ EMAIL TEMPLATE --------------------------------
# ==============================================================================

SUBJECT = "Congratulations! You've been selected for LeadGreen Fellowship Cohort 3"

def get_email_body(name, lab):
    return f"""\
Hello {name},

Congratulations! We are thrilled to inform you that you have been carefully selected from over 6,000 applicants to join the LeadGreen Fellowship Cohort 3.

You have been assigned to the {lab} based on your profile and interests.

We will follow up shortly with the onboarding steps and instructions on accessing your Alumni profile.

Welcome to the community!

Best regards,
The LeadGreen Team
"""

# ==============================================================================
# ------------------------------ CORE LOGIC ------------------------------------
# ==============================================================================

def load_sent_emails():
    """Load the list of people we've already emailed from previous days."""
    if os.path.exists(TRACKING_FILE):
        with open(TRACKING_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_sent_email(email, sent_list):
    """Save the progress immediately after every email in case it crashes midway."""
    sent_list.add(email)
    with open(TRACKING_FILE, 'w') as f:
        json.dump(list(sent_list), f)

def send_emails():
    # 1. Load previously sent emails
    sent_emails = load_sent_emails()
    
    # 2. Read the exported CSV
    try:
        with open(CSV_FILE_PATH, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            applicants = list(reader)
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{CSV_FILE_PATH}'.")
        print("Make sure you exported the CSV from the dashboard and renamed it exactly as set in the configuration above.")
        return
        
    print(f"📊 Total applicants in CSV: {len(applicants)}")
    print(f"📧 Emails already sent from previous days: {len(sent_emails)}")
    
    # 3. Connect to Google SMTP
    try:
        print("\n⏳ Connecting to Gmail SMTP Server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        print("✅ Successfully authenticated with Gmail!\n")
    except Exception as e:
        print(f"❌ Login Failed: {e}")
        print("Important: Did you generate an 'App Password' from Google Security settings? Normal passwords do not work for SMTP.")
        return

    # 4. Start the Drip Campaign
    sent_today = 0
    
    for row in applicants:
        # The exported CSV has headers: Name, Email, Gender, Country, Phone Number, Climate Action Lab
        email = row.get("Email", "").strip().lower()
        name = row.get("Name", "Fellow").strip()
        lab = row.get("Climate Action Lab", "General Fellowship").strip()
        
        if not email or email in sent_emails:
            continue
            
        if sent_today >= MAX_EMAILS_PER_RUN:
            print(f"\n✋ Reached the safe daily limit of {MAX_EMAILS_PER_RUN} emails.")
            print("Please run this exact script again tomorrow to continue sending the rest.")
            break
            
        # Construct Email Message
        msg = EmailMessage()
        msg['Subject'] = SUBJECT
        msg['From'] = f"LeadGreen <{EMAIL_ADDRESS}>"
        msg['To'] = email
        msg.set_content(get_email_body(name, lab))
        
        # Send Email
        try:
            server.send_message(msg)
            print(f"[{sent_today + 1}] Sent successfully to: {email} ({name})")
            
            # Save our place
            save_sent_email(email, sent_emails)
            sent_today += 1
            
            # Very important: Wait for 2 seconds. Google thinks you are a malicious bot if you blast emails at 1,000 per second.
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Failed to send to {email}: {e}")
            break
            
    # Cleanup
    server.quit()
    print(f"\n======================================")
    print(f"🏁 Finished run! Total emails sent today: {sent_today}")
    print(f"======================================")
    
if __name__ == "__main__":
    send_emails()
