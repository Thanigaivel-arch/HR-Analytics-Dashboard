# DATA QUALITY AND INTEGRITY REPORT

Generated at: 2026-08-23 22:34:06

## 1. Duplicate Records Inspection
- Success: No duplicate Employee_IDs found in employees.csv.
- Success: No duplicate Candidate_IDs found in recruitment.csv.
- Success: No duplicate review events (Employee + Date) found in performance.csv.

## 2. Missing Value Analysis
- Missing critical values in employees.csv:
Series([], )
- Exit_Date missing fields: 1725 total. Active employees with missing Exit_Date: 1725 of 1725 (Expected).
- Missing critical values in recruitment.csv:
Series([], )
- Missing critical values in performance.csv:
Series([], )

## 3. Logical Date and Range Checks
- Success: All Exit_Dates are after Joining_Dates.
- Success: No future hiring/joining dates in employees.csv.

## 4. Value Ranges and Integrity Checks
- Employees with unrealistic ages (<18 or >70): 0
- Success: Experience years correspond logically to employee ages.
- Employees with invalid salaries (<= 0): 0
- Employees with invalid Satisfaction Score (not 1-5): 0
- Employees with invalid Performance Score (not 1-5): 0
- Success: Employee statuses are fully aligned with exit date values.

## 5. Referential Integrity Check
- Success: All Employee IDs in performance reviews refer to valid employees.

## Summary Table Stats
- Total Cleaned Employees: 2200
- Total Cleaned Recruitment Records: 650
- Total Cleaned Performance Reviews: 5954