import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Ensure folders exist
os.makedirs('data', exist_ok=True)
os.makedirs('python', exist_ok=True)

# --- Configuration & Master Data ---
DEPARTMENTS = ['IT', 'HR', 'Finance', 'Sales', 'Marketing', 'Operations', 'Customer Service']

JOB_ROLES = {
    'IT': ['Software Engineer', 'Senior Developer', 'System Administrator', 'QA Engineer', 'Data Scientist'],
    'HR': ['HR Generalist', 'Talent Acquisition Specialist', 'HR Manager', 'Benefits Specialist'],
    'Finance': ['Financial Analyst', 'Senior Accountant', 'Finance Manager', 'Auditor'],
    'Sales': ['Sales Representative', 'Account Manager', 'Sales Director', 'Business Development Associate'],
    'Marketing': ['Marketing Specialist', 'Digital Marketing Manager', 'Brand Manager', 'Content Writer'],
    'Operations': ['Operations Analyst', 'Logistics Coordinator', 'Operations Manager', 'Supply Chain Planner'],
    'Customer Service': ['Customer Support Agent', 'Support Lead', 'Customer Success Manager']
}

LOCATIONS = ['New York', 'San Francisco', 'Chicago', 'Austin', 'Atlanta', 'Boston', 'Seattle']
EDUCATION_LEVELS = ["Bachelor's", "Master's", "MBA", "PhD"]
RECRUITMENT_SOURCES = ['LinkedIn', 'Indeed', 'Glassdoor', 'Referral', 'College Campus', 'Executive Search']

BASE_SALARIES = {
    # IT
    'Software Engineer': (65000, 95000),
    'Senior Developer': (105000, 150000),
    'System Administrator': (60000, 85000),
    'QA Engineer': (55000, 80000),
    'Data Scientist': (80000, 130000),
    # HR
    'HR Generalist': (45000, 65000),
    'Talent Acquisition Specialist': (48000, 70000),
    'HR Manager': (80000, 115000),
    'Benefits Specialist': (50000, 72000),
    # Finance
    'Financial Analyst': (58000, 88000),
    'Senior Accountant': (70000, 95000),
    'Finance Manager': (90000, 135000),
    'Auditor': (55000, 80000),
    # Sales
    'Sales Representative': (40000, 65000),  # Base. Commissions reflected in final salary calculations
    'Account Manager': (60000, 90000),
    'Sales Director': (110000, 175000),
    'Business Development Associate': (45000, 68000),
    # Marketing
    'Marketing Specialist': (48000, 72000),
    'Digital Marketing Manager': (75000, 110000),
    'Brand Manager': (80000, 120000),
    'Content Writer': (40000, 60000),
    # Operations
    'Operations Analyst': (50000, 75000),
    'Logistics Coordinator': (45000, 65000),
    'Operations Manager': (85000, 125000),
    'Supply Chain Planner': (55000, 80000),
    # Customer Service
    'Customer Support Agent': (35000, 50000),
    'Support Lead': (50000, 70000),
    'Customer Success Manager': (60000, 90000)
}

# --- Data Generation Helper Functions ---

def random_date(start, end):
    """Generate a random datetime between two datetime objects."""
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

def generate_employee_dataset(num_employees=2200):
    start_date_range = datetime(2020, 1, 1)
    end_date_range = datetime(2026, 6, 30)
    current_time = datetime(2026, 8, 23)

    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth",
                   "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
                   "Christopher", "Nancy", "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra",
                   "Donald", "Ashley", "Steven", "Dorothy", "Paul", "Kimberly", "Andrew", "Emily", "Joshua", "Donna",
                   "Kenneth", "Michelle", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa", "Timothy", "Deborah"]
    
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
                  "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
                  "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
                  "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter", "Roberts"]

    employees = []
    
    for i in range(1, num_employees + 1):
        emp_id = f"EMP{i:04d}"
        gender = random.choice(['Male', 'Female', 'Non-binary'])
        
        # Pick names
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        emp_name = f"{fname} {lname}"
        
        # Education and Age consistency
        education = random.choices(EDUCATION_LEVELS, weights=[0.5, 0.3, 0.15, 0.05])[0]
        min_age = 21
        if education == "Master's" or education == "MBA":
            min_age = 23
        elif education == "PhD":
            min_age = 26
            
        age = int(np.random.normal(37, 9))
        age = max(min_age, min(age, 65))
        
        # Experience consistency
        max_exp = age - min_age
        exp_years = max(0, int(np.random.beta(2, 5) * max_exp))
        if exp_years > 40:
            exp_years = 40
            
        # Department and Job Role
        dept = random.choice(DEPARTMENTS)
        role = random.choice(JOB_ROLES[dept])
        
        # Location & Location multiplier for salary
        location = random.choice(LOCATIONS)
        loc_multiplier = 1.25 if location in ['New York', 'San Francisco', 'Seattle'] else 1.0
        
        # Calculate Salary base on role, experience, and location
        base_min, base_max = BASE_SALARIES[role]
        exp_multiplier = 1.0 + (exp_years * 0.04) # 4% raise per year of experience
        salary = int(random.randint(base_min, base_max) * exp_multiplier * loc_multiplier)
        
        # Joining Date
        join_date = random_date(start_date_range, end_date_range)
        
        # Attrition Logic (determine Status and Exit_Date)
        # Baseline probability of leaving is 12%
        exit_prob = 0.12
        
        # Attrition correlations:
        if dept in ['Sales', 'Customer Service']:
            exit_prob += 0.10 # High turnover depts
        if dept == 'Finance':
            exit_prob -= 0.04 # Low turnover depts
            
        # We will determine satisfaction and performance scores first, as they influence attrition
        # Satisfactions (1 to 5)
        satisfaction = random.choices([1, 2, 3, 4, 5], weights=[0.08, 0.15, 0.45, 0.22, 0.10])[0]
        # Performance (1 to 5)
        performance = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.12, 0.50, 0.23, 0.10])[0]
        
        if satisfaction <= 2:
            exit_prob += 0.25 # Unsatisfied employees are highly likely to leave
        if performance == 1:
            exit_prob += 0.20 # Poor performers are let go
        if performance == 5:
            exit_prob -= 0.05 # Top performers are retained
            
        # Overtime hours (0 to 200) - more overtime -> higher exit prob, lower satisfaction
        overtime = int(max(0, np.random.normal(40, 50)))
        if overtime > 120:
            exit_prob += 0.12
            if satisfaction > 1:
                satisfaction -= 1 # Overtime drags down satisfaction
                
        # Absenteeism (0 to 30) - high absenteeism -> lower satisfaction/performance
        absenteeism = int(max(0, np.random.normal(5, 4)))
        if absenteeism > 15:
            if performance > 1:
                performance -= 1
            if satisfaction > 1:
                satisfaction -= 1
            exit_prob += 0.15
            
        # Recruitment source
        source = random.choices(RECRUITMENT_SOURCES, weights=[0.35, 0.25, 0.15, 0.12, 0.10, 0.03])[0]
        if source == 'Referral':
            satisfaction = min(5, satisfaction + 1)
            exit_prob -= 0.05
            
        # Training Hours (0 to 100) - training helps performance
        training = int(max(0, min(100, np.random.normal(30, 20))))
        if training > 60:
            performance = min(5, performance + 1)
            
        # Enforce exit decision
        status = 'Active'
        exit_date = None
        
        # Employees joining very recently (within past 3 months) can't have left yet in our logic
        days_since_joining = (current_time - join_date).days
        if days_since_joining < 90:
            exit_prob = 0.0
            
        if random.random() < exit_prob and days_since_joining >= 90:
            status = 'Left'
            # Exit date is random date between join_date + 60 days and current_time
            min_exit = join_date + timedelta(days=60)
            exit_date = random_date(min_exit, current_time)
            
        employees.append({
            'Employee_ID': emp_id,
            'Employee_Name': emp_name,
            'Age': age,
            'Gender': gender,
            'Department': dept,
            'Job_Role': role,
            'Education': education,
            'Experience_Years': exp_years,
            'Joining_Date': join_date.strftime('%Y-%m-%d'),
            'Exit_Date': exit_date.strftime('%Y-%m-%d') if exit_date else '',
            'Employment_Status': status,
            'Salary': salary,
            'Performance_Score': performance,
            'Satisfaction_Score': satisfaction,
            'Training_Hours': training,
            'Absenteeism_Days': absenteeism,
            'Overtime_Hours': overtime,
            'Recruitment_Source': source,
            'Location': location
        })
        
    return pd.DataFrame(employees)

def generate_recruitment_dataset(num_candidates=650, emp_df=None):
    candidates = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2026, 8, 20)
    
    # We will ensure some candidates are marked "Joined" and align with the newest employees
    newly_joined_emps = []
    if emp_df is not None:
        newly_joined_emps = emp_df[emp_df['Joining_Date'] >= '2025-01-01'].to_dict('records')
    
    joined_idx = 0
    
    for i in range(1, num_candidates + 1):
        cand_id = f"CAND{i:04d}"
        
        # Link to actual employee if we want to simulate realistic Joined status
        if joined_idx < len(newly_joined_emps) and random.random() < 0.35:
            # Recreate candidate record based on actual joined employee
            emp = newly_joined_emps[joined_idx]
            joined_idx += 1
            
            dept = emp['Department']
            role = emp['Job_Role']
            source = emp['Recruitment_Source']
            exp_years = emp['Experience_Years']
            
            hiring_date_dt = datetime.strptime(emp['Joining_Date'], '%Y-%m-%d')
            time_to_hire = random.randint(15, 60)
            app_date_dt = hiring_date_dt - timedelta(days=time_to_hire)
            
            status = 'Joined'
            interview_score = random.randint(75, 98)
            offered_salary = emp['Salary']
            expected_salary = int(offered_salary * random.uniform(0.9, 1.05))
            rec_cost = calculate_rec_cost(source)
            hiring_date = emp['Joining_Date']
        else:
            # Standalone candidate
            dept = random.choice(DEPARTMENTS)
            role = random.choice(JOB_ROLES[dept])
            source = random.choice(RECRUITMENT_SOURCES)
            exp_years = int(max(0, np.random.normal(5, 4)))
            
            app_date_dt = random_date(start_date, end_date)
            status = random.choices(
                ['Applied', 'Shortlisted', 'Interviewed', 'Selected', 'Rejected'], 
                weights=[0.30, 0.20, 0.20, 0.10, 0.20]
            )[0]
            
            interview_score = random.randint(30, 95)
            # Filter score logically
            if status in ['Selected', 'Shortlisted'] and interview_score < 65:
                interview_score += 20
            if status == 'Rejected' and interview_score > 75:
                interview_score -= 20
                
            base_min, base_max = BASE_SALARIES[role]
            expected_salary = int(random.randint(base_min, base_max) * (1.0 + exp_years*0.04))
            
            if status == 'Selected':
                offered_salary = int(expected_salary * random.uniform(0.95, 1.05))
                time_to_hire = random.randint(20, 75)
                hiring_date_dt = app_date_dt + timedelta(days=time_to_hire)
                hiring_date = hiring_date_dt.strftime('%Y-%m-%d')
            else:
                offered_salary = 0
                time_to_hire = None
                hiring_date = ''
                
            rec_cost = calculate_rec_cost(source) if status in ['Selected', 'Joined'] else int(calculate_rec_cost(source) * 0.1)

        candidates.append({
            'Candidate_ID': cand_id,
            'Application_Date': app_date_dt.strftime('%Y-%m-%d'),
            'Department': dept,
            'Job_Role': role,
            'Recruitment_Source': source,
            'Candidate_Status': status,
            'Interview_Score': interview_score,
            'Experience_Years': exp_years,
            'Expected_Salary': expected_salary,
            'Offered_Salary': offered_salary,
            'Hiring_Date': hiring_date,
            'Time_to_Hire': time_to_hire if time_to_hire else '',
            'Recruitment_Cost': rec_cost
        })
        
    return pd.DataFrame(candidates)

def calculate_rec_cost(source):
    if source == 'Executive Search':
        return random.randint(12000, 25000)
    elif source == 'LinkedIn':
        return random.randint(1500, 4500)
    elif source == 'Indeed':
        return random.randint(800, 2500)
    elif source == 'Glassdoor':
        return random.randint(1000, 3000)
    elif source == 'College Campus':
        return random.randint(500, 2000)
    else: # Referral
        return random.randint(300, 1000)

def generate_performance_dataset(emp_df):
    performance_records = []
    
    for index, emp in emp_df.iterrows():
        emp_id = emp['Employee_ID']
        join_date = datetime.strptime(emp['Joining_Date'], '%Y-%m-%d')
        exit_date_str = emp['Exit_Date']
        
        if exit_date_str:
            last_date = datetime.strptime(exit_date_str, '%Y-%m-%d')
        else:
            last_date = datetime(2026, 8, 23)
            
        tenure_days = (last_date - join_date).days
        num_reviews = tenure_days // 365
        
        if num_reviews == 0 and tenure_days > 180:
            num_reviews = 1
            
        for review_num in range(1, num_reviews + 1):
            review_date = join_date + timedelta(days=review_num * 365)
            
            if review_date >= last_date:
                review_date = last_date - timedelta(days=15)
                if review_date <= join_date:
                    continue
            
            perf_base = emp['Performance_Score']
            sat_base = emp['Satisfaction_Score']
            
            training_hours = int(max(0, min(100, np.random.normal(emp['Training_Hours'] / (num_reviews if num_reviews > 0 else 1), 10))))
            
            perf_score = int(max(1, min(5, np.random.normal(perf_base, 0.6))))
            sat_score = int(max(1, min(5, np.random.normal(sat_base, 0.6))))
            
            goals_achieved = int(min(110, max(40, np.random.normal(70 + (perf_score * 7), 12))))
            manager_rating = int(max(1, min(5, np.random.normal(perf_score, 0.5))))
            
            promotion = 'No'
            if perf_score >= 4 and random.random() < 0.15:
                promotion = 'Yes'
                
            performance_records.append({
                'Employee_ID': emp_id,
                'Review_Date': review_date.strftime('%Y-%m-%d'),
                'Performance_Score': perf_score,
                'Satisfaction_Score': sat_score,
                'Training_Hours': training_hours,
                'Goals_Achieved': goals_achieved,
                'Manager_Rating': manager_rating,
                'Promotion_Status': promotion
            })
            
    return pd.DataFrame(performance_records)

# --- Execution ---
if __name__ == '__main__':
    print("Generating synthetic datasets...")
    
    # 1. Employees
    emp_df = generate_employee_dataset(2200)
    emp_df.to_csv('data/employees.csv', index=False)
    print(f"Generated {len(emp_df)} employee records in data/employees.csv")
    
    # 2. Recruitment
    rec_df = generate_recruitment_dataset(650, emp_df)
    rec_df.to_csv('data/recruitment.csv', index=False)
    print(f"Generated {len(rec_df)} recruitment records in data/recruitment.csv")
    
    # 3. Performance
    perf_df = generate_performance_dataset(emp_df)
    perf_df.to_csv('data/performance.csv', index=False)
    print(f"Generated {len(perf_df)} performance review records in data/performance.csv")
    
    print("\nDataset generation completed successfully!")
