import csv
import random

input_file = r"c:\Users\OLUGBADE TAYO\Desktop\AI coding class\LeadGreen V1\LeadGreen_All_Applications.csv"
leads_file = r"c:\Users\OLUGBADE TAYO\Desktop\AI coding class\LeadGreen V1\Selected_Leads.csv"
output_file = r"c:\Users\OLUGBADE TAYO\Desktop\AI coding class\LeadGreen V1\Selected_Fellows.csv"

LABS = [
    "Climate Adaptation Lab",
    "Climate Mitigation Lab",
    "Renewable Energy Lab",
    "Clean Energy Access Lab",
    "Energy Efficiency Lab",
    "Waste Management Lab",
    "Plastic Pollution Lab",
    "Circular Economy Lab",
    "Recycling Lab",
    "Sustainable Agriculture Lab",
    "Food Systems Lab",
    "Reforestation Lab",
    "Biodiversity Lab",
    "Land Restoration Lab",
    "Water Security Lab",
    "Sustainable Cities Lab",
    "Green Infrastructure Lab",
    "Sustainable Mobility Lab",
    "Clean Air Lab",
    "Climate & Health Lab",
    "Climate Education Lab",
    "Climate Storytelling Lab",
    "Climate Policy Lab",
    "Climate Justice Lab",
    "Youth Leadership Lab",
    "Climate Finance Lab",
    "Green Enterprise Lab",
    "Climate Technology Lab",
    "Climate Resilience Lab",
    "Ocean & Coastal Lab"
]

def main():
    # 1. Read existing leads to exclude them
    leads_emails = set()
    try:
        with open(leads_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = (row.get('Email') or '').strip().lower()
                if email:
                    leads_emails.add(email)
    except FileNotFoundError:
        pass
        
    fellows = []
    # 2. Read all applications and select fellows
    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email_raw = row.get('Email') or ''
            email = email_raw.strip().lower()
            
            # Skip if they are already leads
            if email in leads_emails and email != '':
                continue 
            
            first_name = (row.get('First Name') or '').strip()
            last_name = (row.get('Last Name') or '').strip()
            name = f"{first_name} {last_name}".strip()
            country = (row.get('Country') or '').strip()
            # Assuming phone number is listed under WhatsApp column based on data
            phone = (row.get('WhatsApp') or '').strip()
            
            # Randomly pick a lab
            lab = random.choice(LABS)
            
            fellow_record = {
                'Name': name,
                'Email': email_raw.strip(),
                'Country': country,
                'Phone Number': phone,
                'Climate Action Lab': lab
            }
            fellows.append(fellow_record)

    # 3. Write output
    out_fieldnames = ['Name', 'Email', 'Country', 'Phone Number', 'Climate Action Lab']
    with open(output_file, mode='w', encoding='utf-8', newline='') as out_f:
        writer = csv.DictWriter(out_f, fieldnames=out_fieldnames)
        writer.writeheader()
        for f in fellows:
            writer.writerow(f)
            
    print(f"Successfully processed {len(fellows)} general fellows.")
    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    main()
