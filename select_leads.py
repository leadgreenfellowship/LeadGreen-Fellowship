import csv
import os
import random

input_file = r"c:\Users\OLUGBADE TAYO\Downloads\LeadGreen_All_Applications (1).csv"
output_file = r"c:\Users\OLUGBADE TAYO\Desktop\AI coding class\LeadGreen V1\Selected_Leads.csv"

LABS = [
    ("01", "Climate Adaptation Lab"),
    ("02", "Climate Mitigation Lab"),
    ("03", "Renewable Energy Lab"),
    ("04", "Clean Energy Access Lab"),
    ("05", "Energy Efficiency Lab"),
    ("06", "Waste Management Lab"),
    ("07", "Plastic Pollution Lab"),
    ("08", "Circular Economy Lab"),
    ("09", "Recycling Lab"),
    ("10", "Sustainable Agriculture Lab"),
    ("11", "Food Systems Lab"),
    ("12", "Reforestation Lab"),
    ("13", "Biodiversity Lab"),
    ("14", "Land Restoration Lab"),
    ("15", "Water Security Lab"),
    ("16", "Sustainable Cities Lab"),
    ("17", "Green Infrastructure Lab"),
    ("18", "Sustainable Mobility Lab"),
    ("19", "Clean Air Lab"),
    ("20", "Climate & Health Lab"),
    ("21", "Climate Education Lab"),
    ("22", "Climate Storytelling Lab"),
    ("23", "Climate Policy Lab"),
    ("24", "Climate Justice Lab"),
    ("25", "Youth Leadership Lab"),
    ("26", "Climate Finance Lab"),
    ("27", "Green Enterprise Lab"),
    ("28", "Climate Technology Lab"),
    ("29", "Climate Resilience Lab"),
    ("30", "Ocean & Coastal Lab")
]

def calculate_score(row):
    score = 0
    # Add length of text fields as a heuristic for detail/effort
    text_fields = ['Impact Experience', 'Leadership Experience', 'Why LeadGreen', 'Proposed Project', 'Leadership Style']
    for field in text_fields:
        val = row.get(field)
        if val:
            score += len(str(val))
    return score

try:
    with open(input_file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        males = []
        females = []
        
        for row in reader:
            gender = (row.get('Gender') or '').strip().lower()
            lead_interest = (row.get('Lead Interest') or '').strip().lower()
            try:
                age = int(row.get('Age', 0) or 0)
            except ValueError:
                age = 0
            
            # Apply age constraints: over 25 and not above 30
            # Ensure applicant selected specifically indicated 'Yes' to Lead Interest
            if age > 25 and age <= 30 and lead_interest == 'yes':
                score = calculate_score(row)
                row['Score'] = score
                if gender == 'male':
                    males.append(row)
                elif gender == 'female':
                    females.append(row)

        # Sort by score in descending order
        males.sort(key=lambda x: x['Score'], reverse=True)
        females.sort(key=lambda x: x['Score'], reverse=True)

        top_females = females[:30]
        num_males_needed = 60 - len(top_females)
        top_males = males[:num_males_needed]

        random.shuffle(LABS)

        selected = []
        for i, f in enumerate(top_females):
            f['Role'] = 'Co-Team Lead'
            if i < len(LABS):
                f['Group'] = LABS[i][0]
                f['Climate Action Lab'] = LABS[i][1]
            selected.append(f)
            
        for i, m in enumerate(top_males):
            if i < len(LABS):
                m['Role'] = 'Team Lead'
                m['Group'] = LABS[i][0]
                m['Climate Action Lab'] = LABS[i][1]
            else:
                m['Role'] = 'Co-Team Lead'
                f_missing_idx = len(top_females) + (i - len(LABS))
                if f_missing_idx < len(LABS):
                    m['Group'] = LABS[f_missing_idx][0]
                    m['Climate Action Lab'] = LABS[f_missing_idx][1]
            selected.append(m)
        
        if not selected:
            print("No applicants found!")
        else:
            # Output to CSV
            out_fieldnames = ['Group', 'Climate Action Lab', 'Role', 'Score'] + list(fieldnames)
            with open(output_file, mode='w', encoding='utf-8', newline='') as out_f:
                writer = csv.DictWriter(out_f, fieldnames=out_fieldnames)
                writer.writeheader()
                for row in selected:
                    writer.writerow(row)
            
            print(f"Successfully selected {len(top_males)} male Team Leads and {len(top_females)} female Co-Team Leads.")
            print(f"Results saved to: {output_file}")
except Exception as e:
    import traceback
    traceback.print_exc()
