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
        
    priority_pool = []
    secondary_pool = []
    # 2. Read all applications and select fellows using final criteria
    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email_raw = row.get('Email') or ''
            email = email_raw.strip().lower()
            
            # Criteria 1: Exclude team leads
            if email in leads_emails and email != '':
                continue 
                
            try:
                age = int(row.get('Age', 0) or 0)
            except ValueError:
                age = 0
                
            why_lead = str(row.get('Why LeadGreen') or '').strip()
            env_prob = str(row.get('Environmental Problem') or '').strip()
            gender = str(row.get('Gender') or '').strip().lower()
            country = str(row.get('Country') or '').strip()
            
            # Criteria 2 & 3: Age limit and Basic Knowledge check
            if 18 <= age <= 30 and (len(why_lead) > 5 or len(env_prob) > 5):
                name = f"{(row.get('First Name') or '').strip()} {(row.get('Last Name') or '').strip()}".strip()
                phone = (row.get('WhatsApp') or '').strip()
                
                fellow_record = {
                    'Name': name,
                    'Email': email_raw.strip(),
                    'Country': country,
                    'Phone Number': phone
                }
                
                # Criteria 4: Priority placing
                if gender == 'female' or country.lower() != 'nigeria':
                    priority_pool.append(fellow_record)
                else:
                    secondary_pool.append(fellow_record)

    # Criteria 5: Randomly shuffle and truncate up to 3000
    random.shuffle(priority_pool)
    random.shuffle(secondary_pool)
    
    fellows = []
    for app in priority_pool:
        if len(fellows) < 3000:
            app['Climate Action Lab'] = random.choice(LABS)
            fellows.append(app)
            
    for app in secondary_pool:
        if len(fellows) < 3000:
            app['Climate Action Lab'] = random.choice(LABS)
            fellows.append(app)

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
