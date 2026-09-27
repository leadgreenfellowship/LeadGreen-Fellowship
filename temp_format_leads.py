import csv

file_path = "C:/Users/OLUGBADE TAYO/Desktop/AI coding class/LeadGreen V1/Selected_Leads.csv"
out_path = "C:/Users/OLUGBADE TAYO/.gemini/antigravity/brain/447f50ae-7235-4dfd-8e3c-8a41e850ec09/Leads_List.md"

leads = []
with open(file_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        role = row.get("Role", "")
        name = f"{row.get('First Name', '')} {row.get('Last Name', '')}".strip()
        lab = row.get("Climate Action Lab", "Unassigned Lab")
        leads.append((name, role, lab))

leads.sort(key=lambda x: (x[2], x[1], x[0]))

with open(out_path, mode='w', encoding='utf-8') as out_f:
    out_f.write(f"Total Selected Leads: {len(leads)}\n\n")
    out_f.write("| Name | Role | Action Lab |\n")
    out_f.write("|---|---|---|\n")
    for n, r, l in leads:
        out_f.write(f"| {n} | {r} | {l} |\n")
