import csv
import json
import hashlib
import requests
import time

API_KEY = "AIzaSyA5lPT8Fyp265fvebWq4BelNE0dYxuWvCE"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/leadgreen-fellowship/databases/(default)/documents/certificate_payments?key={API_KEY}"

def get_existing_records():
    existing_emails = set()
    url = f"{BASE_URL}&pageSize=300"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            docs = data.get("documents", [])
            for doc in docs:
                fields = doc.get("fields", {})
                if "email" in fields:
                    em = fields["email"].get("stringValue", "").strip().lower()
                    if em:
                        existing_emails.add(em)
            print(f"Found {len(existing_emails)} existing paid emails in Firestore.")
        else:
            print("Warning: Could not fetch existing records:", resp.text)
    except Exception as e:
        print("Error fetching records:", e)
    return existing_emails

def load_csv_fellows():
    fellows = {}
    
    # 1. Load Allpaidfellows.csv
    try:
        with open("Allpaidfellows.csv", mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                email = (r.get("Customer Email") or "").strip().lower()
                name = (r.get("Customer Fullname") or "").strip()
                if email and "@" in email:
                    fellows[email] = {
                        "email": email,
                        "fullName": name or "LeadGreen Fellow",
                        "reference": f"LG-REC-{hashlib.md5(email.encode()).hexdigest()[:8].upper()}",
                        "amount": 1.99,
                        "currency": "USD"
                    }
    except Exception as e:
        print("Error reading Allpaidfellows.csv:", e)

    # 2. Load sales report if available
    try:
        with open("sales_report_2026_10_07_10_20.csv", mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                email = (r.get("Customer Email") or "").strip().lower()
                name = (r.get("Customer Fullname") or "").strip()
                ref = (r.get("Reference") or "").strip()
                total = r.get("Total") or "1.99"
                curr = r.get("Currency") or "USD"
                try:
                    amount = float(total)
                except:
                    amount = 1.99
                if email and "@" in email:
                    fellows[email] = {
                        "email": email,
                        "fullName": name or fellows.get(email, {}).get("fullName", "LeadGreen Fellow"),
                        "reference": ref or fellows.get(email, {}).get("reference", f"LG-REC-{hashlib.md5(email.encode()).hexdigest()[:8].upper()}"),
                        "amount": amount if amount > 0 else 1.99,
                        "currency": curr
                    }
    except Exception as e:
        print("Error reading sales report:", e)

    return list(fellows.values())

def sync_fellows():
    existing_emails = get_existing_records()
    csv_fellows = load_csv_fellows()
    print(f"Total fellows from CSV files: {len(csv_fellows)}")

    synced_count = 0
    skipped_count = 0

    for fellow in csv_fellows:
        email = fellow["email"]
        if email in existing_emails:
            skipped_count += 1
            continue

        doc_id = fellow["reference"]
        doc_url = f"https://firestore.googleapis.com/v1/projects/leadgreen-fellowship/databases/(default)/documents/certificate_payments/{doc_id}?key={API_KEY}"

        payload = {
            "fields": {
                "fullName": {"stringValue": fellow["fullName"]},
                "email": {"stringValue": email},
                "paymentReference": {"stringValue": doc_id},
                "amount": {"doubleValue": float(fellow["amount"])},
                "currency": {"stringValue": fellow["currency"]},
                "status": {"stringValue": "paid"}
            }
        }

        try:
            resp = requests.patch(doc_url, data=json.dumps(payload), headers={"Content-Type": "application/json"})
            if resp.status_code == 200:
                synced_count += 1
                existing_emails.add(email)
                print(f"[{synced_count}] Synced: {fellow['fullName']} <{email}>")
            else:
                print(f"Failed to sync {email}: {resp.status_code} - {resp.text}")
            time.sleep(0.05)
        except Exception as e:
            print(f"Exception syncing {email}: {e}")

    print("\n--- SYNC SUMMARY ---")
    print(f"Already in database: {skipped_count}")
    print(f"Newly synced records: {synced_count}")
    print(f"Total paid fellows in database now: {len(existing_emails)}")

if __name__ == "__main__":
    sync_fellows()
