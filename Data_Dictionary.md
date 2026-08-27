# Data Dictionary

This document details the schema definitions for the three generated datasets (`employees.csv`, `recruitment.csv`, `performance.csv`) and the forecast dataset (`hiring_forecast_output.csv`) used in the Human Resources Analytics & Workforce Intelligence project.

---

## 1. Table: Fact_Employees (`employees.csv`)
This table represents the master record of all active and former employees in the organization.

| Column Name | Data Type | Description | Example | Purpose / Business Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Employee_ID** | Text | Unique identifier for each employee. | `EMP0001` | Primary Key. Links to the Performance table. |
| **Employee_Name** | Text | The full name of the employee. | `James Smith` | Profile detail. Displayed in employee search tables. |
| **Age** | Integer | The age of the employee in years. | `34` | Demographic profiling. Used to calculate average workforce age. |
| **Gender** | Text | The gender category of the employee. | `Female` | Diversity & Inclusion (D&I) metric. |
| **Department** | Text | The organizational department the employee belongs to. | `IT` | Dimensional grouping for salary, attrition, performance, etc. |
| **Job_Role** | Text | The specific position name. | `Software Engineer` | Job tier mapping and average compensation analysis. |
| **Education** | Text | Highest education level attained. | `Master's` | Workforce skill evaluation and qualification screening. |
| **Experience_Years** | Integer | Number of years of professional work experience. | `8` | Career level mapping, correlates with salary. |
| **Joining_Date** | Date | The date the employee was hired and joined. | `2021-04-15` | Baseline date for tenure calculation and hiring trends. |
| **Exit_Date** | Date | The date the employee left the company (if applicable). | `2024-11-20` | Determines employee termination date and total tenure. |
| **Employment_Status**| Text | Current work status: 'Active' or 'Left'. | `Active` | Crucial status filter. Splits active workforce from exits. |
| **Salary** | Integer | The employee's annual base salary in USD. | `85000` | Basic compensation. Used to calculate payroll expenses. |
| **Performance_Score**| Integer | Current overall performance rating (1 to 5). | `4` | Career rating. 1=Poor, 3=Meets, 5=Outstanding. |
| **Satisfaction_Score**| Integer | Employee satisfaction score (1 to 5). | `3` | Engagement metric. 1=Dissatisfied, 5=Highly Satisfied. |
| **Training_Hours** | Integer | Hours of training completed in the current cycle. | `45` | Career development and upskilling measure. |
| **Absenteeism_Days**| Integer | Days absent during the year (sick/unexcused). | `4` | Absenteeism tracking. Linked to employee engagement. |
| **Overtime_Hours** | Integer | Total overtime hours worked in the year. | `120` | Workload mapping. High overtime correlates with attrition. |
| **Recruitment_Source**| Text | Channels through which the employee was hired. | `LinkedIn` | ROI tracking of recruiting channels. |
| **Location** | Text | The geographic office where employee is located. | `Austin` | Geographical distribution analysis. |

---

## 2. Table: Fact_Recruitment (`recruitment.csv`)
This table tracks all job applications, selection cycles, and candidate pipelines.

| Column Name | Data Type | Description | Example | Purpose / Business Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Candidate_ID** | Text | Unique identifier for each candidate. | `CAND0001` | Primary Key for candidate analysis. |
| **Application_Date**| Date | Date the candidate submitted their application. | `2022-01-10` | Sourcing timeline tracker. |
| **Department** | Text | The department the candidate applied for. | `Sales` | Departmental hiring pipeline volume. |
| **Job_Role** | Text | The job role applied for. | `Sales Representative`| Specific position demand monitoring. |
| **Recruitment_Source**| Text | Sourcing channel of the application. | `Indeed` | Evaluates channel application volume. |
| **Candidate_Status**| Text | Application stage: Applied, Shortlisted, etc. | `Joined` | Tracks recruitment funnel conversion rate. |
| **Interview_Score** | Integer | Score out of 100 in the interview stage. | `85` | Standardized test of candidate quality. |
| **Experience_Years**| Integer | Candidate's years of professional experience. | `4` | Candidate profile evaluation. |
| **Expected_Salary** | Integer | Candidate's desired salary in USD. | `60000` | Tracks candidate market value expectations. |
| **Offered_Salary** | Integer | Salary offer made by the company in USD. | `58000` | Tracks compensation offerings. |
| **Hiring_Date** | Date | Date the candidate accepted/joined (if Joined).| `2022-02-15` | Marks the conclusion of recruitment. |
| **Time_to_Hire** | Integer | Days from Application_Date to Hiring_Date. | `36` | Efficiency metric. Average duration to fill a role. |
| **Recruitment_Cost**| Integer | Financial expense spent on candidate sourcing. | `2000` | Total recruitment cost and cost-per-hire calculations. |

---

## 3. Table: Fact_Performance (`performance.csv`)
This table contains longitudinal records of employee periodic performance reviews.

| Column Name | Data Type | Description | Example | Purpose / Business Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Employee_ID** | Text | Unique identifier referencing Fact_Employees. | `EMP0001` | Foreign Key linking to the master employee record. |
| **Review_Date** | Date | The date on which the review took place. | `2021-12-31` | Slices reviews across chronological intervals (years). |
| **Performance_Score**| Integer | Performance rating given in this review (1 to 5).| `3` | Tracks performance trends over time for an employee. |
| **Satisfaction_Score**| Integer | Satisfaction score reported in this review (1-5).| `4` | Tracks satisfaction fluctuations during tenure. |
| **Training_Hours** | Integer | Training hours completed since last review. | `12` | Short-term training impact on performance reviews. |
| **Goals_Achieved** | Integer | Percentage of objective goals met (%). | `95` | Numeric/quantifiable measure of employee performance. |
| **Manager_Rating** | Integer | Subjective rating from the manager (1 to 5). | `3` | Manager-employee relationship tracking. |
| **Promotion_Status**| Text | Indicating whether the review led to promotion. | `No` | Internal career mobility tracking. |

---

## 4. Table: Fact_HiringForecast (`hiring_forecast_output.csv`)
This table contains aggregated historical hiring numbers combined with 6-month predictive trends.

| Column Name | Data Type | Description | Example | Purpose / Business Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Date** | Date | Year-Month date indicator. | `2026-07-01` | Time dimension for plotting monthly timeline. |
| **Historical_Hires**| Integer | Actual headcount hired during that month. | `25` | Holds historical figures. Blanks for future months. |
| **Forecasted_Hires**| Integer | Predicted headcount required in that month. | `27` | Holds ML-predicted values. Blanks for past dates. |
| **Type** | Text | Denotes dataset row type: 'Actual' or 'Forecast'. | `Forecast` | Slicer/legend label to split actual and predicted lines. |
