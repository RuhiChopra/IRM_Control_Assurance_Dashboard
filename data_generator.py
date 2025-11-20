import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_dr_data(num_apps=50):
    apps = [f"App_{i:03d}" for i in range(1, num_apps + 1)]
    departments = ['Finance', 'HR', 'Trading', 'Compliance', 'Consumer Banking']
    tiers = ['Tier 1 (Critical)', 'Tier 2 (High)', 'Tier 3 (Standard)']
    
    data = []

    for app in apps:
        dept = random.choice(departments)
        tier = random.choice(tiers)
        
        # Logic: Critical apps have tighter RTOs (Recovery Time Objectives)
        if "Tier 1" in tier:
            target_rto = 4 # hours
            target_rpo = 1 # hours
        elif "Tier 2" in tier:
            target_rto = 24
            target_rpo = 12
        else:
            target_rto = 48
            target_rpo = 24
            
        # Simulate Actual Results (some will fail)
        # 15% chance of failure (Actual > Target)
        if random.random() < 0.15:
            actual_rto = target_rto + random.randint(1, 10)
            status = "Fail"
            ticket_needed = True
        else:
            actual_rto = max(0.5, target_rto - random.randint(0, 2))
            status = "Pass"
            ticket_needed = False
            
        # Ticket Management Logic
        ticket_id = "N/A"
        ticket_age = 0
        ticket_status = "N/A"
        
        if ticket_needed:
            ticket_id = f"INC-{random.randint(1000, 9999)}"
            ticket_age = random.randint(1, 120) # Days open
            ticket_status = "Open" if ticket_age < 90 else "Overdue"

        data.append([
            app, dept, tier, target_rto, actual_rto, 
            target_rpo, status, ticket_id, ticket_status, ticket_age
        ])

    columns = [
        'Application Name', 'Department', 'Criticality Tier', 
        'Target RTO (Hrs)', 'Actual RTO (Hrs)', 'Target RPO (Hrs)', 
        'Test Status', 'Remediation Ticket ID', 'Ticket Status', 'Ticket Age (Days)'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    return df

if __name__ == "__main__":
    df = generate_dr_data()
    df.to_csv("dr_compliance_data.csv", index=False)
    print("Data generated: dr_compliance_data.csv")