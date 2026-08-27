import os
import pandas as pd
import numpy as np

def clean_and_verify_data():
    print("Starting data cleaning and quality validation...")
    
    # Check if files exist
    if not (os.path.exists('data/employees.csv') and 
            os.path.exists('data/recruitment.csv') and 
            os.path.exists('data/performance.csv')):
        print("Error: Generated dataset files not found in 'data/' directory. Run data_generation.py first.")
        return
        
    emp_df = pd.read_csv('data/employees.csv')
    rec_df = pd.read_csv('data/recruitment.csv')
    perf_df = pd.read_csv('data/performance.csv')
    
    log_messages = []
    log_messages.append("# DATA QUALITY AND INTEGRITY REPORT\n")
    log_messages.append(f"Generated at: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # ----------------------------------------------------
    # 1. DUPLICATE ID CHECK
    # ----------------------------------------------------
    log_messages.append("## 1. Duplicate Records Inspection")
    
    # Employees duplicates
    emp_dup_ids = emp_df['Employee_ID'].duplicated().sum()
    if emp_dup_ids > 0:
        log_messages.append(f"- WARNING: Found {emp_dup_ids} duplicate Employee_IDs in employees.csv. Removing duplicates...")
        emp_df = emp_df.drop_duplicates(subset=['Employee_ID'], keep='first')
    else:
        log_messages.append("- Success: No duplicate Employee_IDs found in employees.csv.")
        
    # Recruitment duplicates
    rec_dup_ids = rec_df['Candidate_ID'].duplicated().sum()
    if rec_dup_ids > 0:
        log_messages.append(f"- WARNING: Found {rec_dup_ids} duplicate Candidate_IDs in recruitment.csv. Removing duplicates...")
        rec_df = rec_df.drop_duplicates(subset=['Candidate_ID'], keep='first')
    else:
        log_messages.append("- Success: No duplicate Candidate_IDs found in recruitment.csv.")
        
    # Performance duplicates (Employee_ID + Review_Date combination should be unique)
    perf_dup_records = perf_df.duplicated(subset=['Employee_ID', 'Review_Date']).sum()
    if perf_dup_records > 0:
        log_messages.append(f"- WARNING: Found {perf_dup_records} duplicate reviews (same employee and date) in performance.csv. Removing...")
        perf_df = perf_df.drop_duplicates(subset=['Employee_ID', 'Review_Date'], keep='first')
    else:
        log_messages.append("- Success: No duplicate review events (Employee + Date) found in performance.csv.\n")
        
    # ----------------------------------------------------
    # 2. MISSING VALUES CHECK
    # ----------------------------------------------------
    log_messages.append("## 2. Missing Value Analysis")
    
    critical_emp_cols = ['Employee_ID', 'Employee_Name', 'Age', 'Department', 'Job_Role', 'Joining_Date', 'Employment_Status', 'Salary']
    emp_nulls = emp_df[critical_emp_cols].isnull().sum()
    log_messages.append(f"- Missing critical values in employees.csv:\n{emp_nulls[emp_nulls > 0].to_string() or '  None'}")
    
    # Note: Exit_Date null values are expected for active employees
    expected_active_nulls = emp_df[emp_df['Employment_Status'] == 'Active']['Exit_Date'].isnull().sum()
    total_active = (emp_df['Employment_Status'] == 'Active').sum()
    log_messages.append(f"- Exit_Date missing fields: {emp_df['Exit_Date'].isnull().sum()} total. Active employees with missing Exit_Date: {expected_active_nulls} of {total_active} (Expected).")
    
    critical_rec_cols = ['Candidate_ID', 'Application_Date', 'Department', 'Job_Role', 'Recruitment_Source', 'Candidate_Status']
    rec_nulls = rec_df[critical_rec_cols].isnull().sum()
    log_messages.append(f"- Missing critical values in recruitment.csv:\n{rec_nulls[rec_nulls > 0].to_string() or '  None'}")
    
    critical_perf_cols = ['Employee_ID', 'Review_Date', 'Performance_Score', 'Satisfaction_Score', 'Training_Hours', 'Goals_Achieved']
    perf_nulls = perf_df[critical_perf_cols].isnull().sum()
    log_messages.append(f"- Missing critical values in performance.csv:\n{perf_nulls[perf_nulls > 0].to_string() or '  None'}\n")
    
    # ----------------------------------------------------
    # 3. DATE VALIDITY CHECK
    # ----------------------------------------------------
    log_messages.append("## 3. Logical Date and Range Checks")
    
    # Convert date columns to datetime temporarily
    emp_df['Joining_Date_dt'] = pd.to_datetime(emp_df['Joining_Date'])
    emp_df['Exit_Date_dt'] = pd.to_datetime(emp_df['Exit_Date'])
    
    # Check if any Exit_Date is before Joining_Date
    date_violations = emp_df[emp_df['Exit_Date_dt'] < emp_df['Joining_Date_dt']]
    if len(date_violations) > 0:
        log_messages.append(f"- WARNING: Found {len(date_violations)} records where Exit_Date is before Joining_Date! Fixing by clearing Exit_Date and setting status to Active...")
        for idx in date_violations.index:
            emp_df.loc[idx, 'Exit_Date'] = np.nan
            emp_df.loc[idx, 'Employment_Status'] = 'Active'
    else:
        log_messages.append("- Success: All Exit_Dates are after Joining_Dates.")
        
    # Check for future dates
    today = pd.Timestamp.now()
    future_join = emp_df[emp_df['Joining_Date_dt'] > today]
    if len(future_join) > 0:
        log_messages.append(f"- WARNING: Found {len(future_join)} joining dates in the future. Adjusting to today...")
        emp_df.loc[emp_df['Joining_Date_dt'] > today, 'Joining_Date'] = today.strftime('%Y-%m-%d')
    else:
        log_messages.append("- Success: No future hiring/joining dates in employees.csv.\n")
        
    # Remove temp datetime columns
    emp_df = emp_df.drop(columns=['Joining_Date_dt', 'Exit_Date_dt'])
    
    # ----------------------------------------------------
    # 4. RANGE AND SENSITIVITY CHECK (Ages, Ratings, Salary)
    # ----------------------------------------------------
    log_messages.append("## 4. Value Ranges and Integrity Checks")
    
    # Impossible age (< 18 or > 70)
    age_violations = emp_df[(emp_df['Age'] < 18) | (emp_df['Age'] > 70)]
    log_messages.append(f"- Employees with unrealistic ages (<18 or >70): {len(age_violations)}")
    
    # Experience consistency (Age - Experience < 18)
    exp_violations = emp_df[emp_df['Age'] - emp_df['Experience_Years'] < 18]
    if len(exp_violations) > 0:
        log_messages.append(f"- WARNING: Found {len(exp_violations)} cases where Experience_Years exceeds Age-18 bounds. Fixing Experience...")
        emp_df.loc[emp_df['Age'] - emp_df['Experience_Years'] < 18, 'Experience_Years'] = emp_df['Age'] - 18
    else:
        log_messages.append("- Success: Experience years correspond logically to employee ages.")
        
    # Invalid Salaries (<= 0)
    sal_violations = emp_df[emp_df['Salary'] <= 0]
    log_messages.append(f"- Employees with invalid salaries (<= 0): {len(sal_violations)}")
    
    # Invalid Satisfaction/Performance (not between 1 and 5)
    sat_violations = emp_df[~emp_df['Satisfaction_Score'].between(1, 5)]
    perf_violations = emp_df[~emp_df['Performance_Score'].between(1, 5)]
    log_messages.append(f"- Employees with invalid Satisfaction Score (not 1-5): {len(sat_violations)}")
    log_messages.append(f"- Employees with invalid Performance Score (not 1-5): {len(perf_violations)}")
    
    # Status and Exit Date consistency
    status_left_no_exit = emp_df[(emp_df['Employment_Status'] == 'Left') & (emp_df['Exit_Date'].isnull() | (emp_df['Exit_Date'] == ''))]
    status_active_with_exit = emp_df[(emp_df['Employment_Status'] == 'Active') & (emp_df['Exit_Date'].notnull() & (emp_df['Exit_Date'] != ''))]
    
    if len(status_left_no_exit) > 0:
        log_messages.append(f"- WARNING: Found {len(status_left_no_exit)} employees marked 'Left' but missing Exit_Date. Filling with default date...")
        emp_df.loc[(emp_df['Employment_Status'] == 'Left') & (emp_df['Exit_Date'].isnull()), 'Exit_Date'] = '2026-08-23'
    if len(status_active_with_exit) > 0:
        log_messages.append(f"- WARNING: Found {len(status_active_with_exit)} employees marked 'Active' but having an Exit_Date. Clearing Exit_Date...")
        emp_df.loc[emp_df['Employment_Status'] == 'Active', 'Exit_Date'] = np.nan
        
    log_messages.append("- Success: Employee statuses are fully aligned with exit date values.\n")
    
    # ----------------------------------------------------
    # 5. REFERENTIAL INTEGRITY (Relationship Check)
    # ----------------------------------------------------
    log_messages.append("## 5. Referential Integrity Check")
    
    # Check if any Employee_ID in performance table does not exist in employee table
    orphaned_reviews = perf_df[~perf_df['Employee_ID'].isin(emp_df['Employee_ID'])]
    if len(orphaned_reviews) > 0:
        log_messages.append(f"- WARNING: Found {len(orphaned_reviews)} reviews for Employee_IDs that do not exist! Deleting orphaned reviews...")
        perf_df = perf_df[perf_df['Employee_ID'].isin(emp_df['Employee_ID'])]
    else:
        log_messages.append("- Success: All Employee IDs in performance reviews refer to valid employees.")
        
    log_messages.append("\n## Summary Table Stats")
    log_messages.append(f"- Total Cleaned Employees: {len(emp_df)}")
    log_messages.append(f"- Total Cleaned Recruitment Records: {len(rec_df)}")
    log_messages.append(f"- Total Cleaned Performance Reviews: {len(perf_df)}")
    
    # Save back to CSV files
    emp_df.to_csv('data/employees.csv', index=False)
    rec_df.to_csv('data/recruitment.csv', index=False)
    perf_df.to_csv('data/performance.csv', index=False)
    
    # Save log report
    report_content = "\n".join(log_messages)
    os.makedirs('documentation', exist_ok=True)
    with open('documentation/Data_Quality_Report.md', 'w') as f:
        f.write(report_content)
        
    print("\nData cleaning and validation complete!")
    print(f"Report saved to 'documentation/Data_Quality_Report.md'.")
    print(report_content)

if __name__ == '__main__':
    clean_and_verify_data()
