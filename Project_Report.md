# Project Report: Human Resources Analytics & Workforce Intelligence

**Project Title**: Human Resources Analytics & Workforce Intelligence Dashboard  
**Academic Level**: College / Internship Portfolio Project  
**Author**: Junior Data Analyst  
**Mentor/Advisor**: Senior Data Analyst / Power BI Lead  

---

## 1. Abstract
This project presents a comprehensive, data-driven Human Resources (HR) Analytics solution developed to optimize workforce management, enhance recruitment efficiency, reduce employee attrition, and forecast future hiring requirements. Using a generated dataset of 2,200 employees, 650 recruitment records, and 5,954 performance reviews, we built a robust pipeline using Python for data cleaning and predictive modeling (using Linear Regression), and Power BI for data modeling and interactive reporting. The final solution delivers deep tactical insights regarding employee satisfaction, training effectiveness, attrition triggers, and recruitment source efficiency, allowing management to transition from reactive troubleshooting to proactive workforce intelligence.

---

## 2. Introduction
In modern enterprises, human capital is the most critical asset. Organizations spend massive resources on attracting, training, and retaining talent. However, many HR departments continue to operate on intuitive decision-making or fragmented reporting, resulting in high recruitment costs, excessive attrition in critical departments, and uncoordinated training programs. HR Analytics applies data science tools to workforce data, enabling organizations to make objective, data-backed decisions. This project demonstrates how data engineering (cleaning and preprocessing), data science (predictive modeling for forecasting), and business intelligence (Power BI dashboards) can be integrated to solve complex HR challenges.

---

## 3. Problem Statement
The subject organization suffers from several key operational pain points in its workforce management:
1. **Unidentified Attrition Drivers**: High employee turnover is occurring, but the specific drivers (e.g., compensation, manager quality, work-life balance, role, location) have not been quantified.
2. **Recruitment Bottlenecks**: Sourcing channels are not audited for performance, leading to high cost-per-hire and slow time-to-hire in critical business units.
3. **Training & Performance Misalignment**: It is unclear if internal training programs are improving employee performance or satisfaction, or if training budgets are being spent efficiently.
4. **Reactive Hiring**: The organization lacks a reliable mechanism to forecast future hiring requirements, leading to chronic understaffing and high recruitment rushes.

---

## 4. Objectives
The primary objectives of this project are:
* Establish a single source of truth for HR data by designing a professional, optimized star-schema data model.
* Perform data validation and quality cleaning to guarantee report accuracy.
* Calculate core HR metrics and KPIs (Attrition, Hiring Rate, Cost per Hire, Avg tenure) using DAX.
* Create an interactive dashboard with 7 specific reporting pages for executive and operational analysis.
* Build an explainable machine learning model in Python to forecast hiring needs for the next 6 months.
* Translate analytical findings into structured, actionable business recommendations for corporate leadership.

---

## 5. Existing Problem (Pre-analytics)
Before this analytics initiative, HR executives relied on static, monthly spreadsheets. Data was siloed across three different systems:
* An HR Information System (HRIS) tracking core employee profiles.
* An Applicant Tracking System (ATS) containing applicant pipelines.
* A Performance Management System storing annual manager reviews.

Because these tables were never merged, the organization could not correlate recruitment channels with subsequent employee performance, nor could they identify how work hours (overtime) affected attrition. The lack of interactive filters made it impossible for regional directors to drill down into their specific departments, resulting in slow, generalized policy decisions.

---

## 6. Proposed Solution
The proposed solution implements a complete end-to-end data pipeline:
1. **Relational Integration**: Consolidate and link the HRIS (Employees), ATS (Recruitment), and Performance tables.
2. **Quality Verification**: Execute automated Python cleaning scripts to purge duplicate IDs, reconcile age/experience conflicts, and handle date mismatches.
3. **Data Modeling**: Design a Power BI star schema utilizing a central date table (`Dim_Date`) to support cross-filtering.
4. **Calculations**: Implement DAX measures for real-time aggregation of attrition, growth, and costs.
5. **Interactive Dashboard**: Build visualization panels for Executive, Recruitment, Attrition, Performance, Demographics, Forecasting, and Management Insights.
6. **Predictive Analytics**: Develop a simple Linear Regression model in Python to project hiring headcount requirements.

---

## 7. Dataset Specification
The data generated synthetically for this project consists of three relational tables:
* **Fact_Employees** (2,200 rows): Tracks demographic details (Age, Gender, Location, Education), job profiles (Department, Job Role, Salary, Experience), operational inputs (Training Hours, Absenteeism, Overtime), recruitment source, and employment status.
* **Fact_Recruitment** (650 rows): Tracks candidate applications, stages (Applied to Joined), interview scores, expected vs. offered salaries, recruitment costs, and time-to-hire.
* **Fact_Performance** (5,954 rows): Longitudinal panel tracking periodic reviews, recording performance ratings, satisfaction scores, manager ratings, and promotion history.

---

## 8. Data Preparation & Engineering
Data quality is paramount. A dedicated script (`python/data_cleaning.py`) checked and resolved the following anomalies:
* **Duplicate Detection**: Inspected unique keys (`Employee_ID` and `Candidate_ID`). No duplicates were found in our final tables.
* **Logical Consistency Checks**: Checked for impossible ages (none found) and experience years. In cases where experience exceeded the logical age threshold (Age - Experience < 18), the script set `Experience_Years` to `Age - 18`.
* **Status Alignment**: Verified that employees marked 'Left' had a populated `Exit_Date` (and vice-versa). Active employees had their exit dates set to null.
* **Referential Integrity**: Scanned the performance table for orphaned employee IDs. All IDs matched back to the master employee record.
* **Data Quality Report**: Automatically logged findings into a markdown report for documentation.

---

## 9. Data Model Architecture
The database is structured as a **Star Schema** to optimize query performance in Power BI:
* **Fact Tables**:
  * `Fact_Employees`: Slices master active/exited profiles.
  * `Fact_Recruitment`: Slices candidate pipeline details.
  * `Fact_Performance`: Slices longitudinal employee reviews.
* **Dimension Tables**:
  * `Dim_Date`: Standard calendar table containing Year, Quarter, Month, and Week columns.
  * `Fact_HiringForecast`: Forecast output table mapping historical hires and regression forecasts.
* **Relationships**:
  * `Dim_Date[Date]` acts as the master chronological filter. It maintains active links to `Fact_Employees[Joining_Date]`, `Fact_Performance[Review_Date]`, `Fact_Recruitment[Application_Date]`, and `Fact_HiringForecast[Date]`.
  * Inactive relationships are established with `Fact_Employees[Exit_Date]` and `Fact_Recruitment[Hiring_Date]` to allow target calculations using `USERELATIONSHIP()`.
  * `Fact_Employees[Employee_ID]` connects to `Fact_Performance[Employee_ID]` in a 1-to-many relationship.

---

## 10. DAX Measures Compilation
Key measures written to execute calculations include:
* **Active Headcount**: `Active Employees = CALCULATE(COUNTROWS(Fact_Employees), Fact_Employees[Employment_Status] = "Active")`
* **Attrition Rate**: `Attrition Rate = DIVIDE(CALCULATE(COUNTROWS(Fact_Employees), Fact_Employees[Employment_Status] = "Left"), COUNTROWS(Fact_Employees), 0)`
* **Average Time to Hire**: `Average Time to Hire = AVERAGE(Fact_Recruitment[Time_to_Hire])`
* **Hiring Rate**: `Hiring Rate = DIVIDE(CALCULATE(COUNTROWS(Fact_Recruitment), Fact_Recruitment[Candidate_Status] = "Joined"), COUNTROWS(Fact_Recruitment), 0)`
* **YoY Employee Growth**: Computes current active headcount vs. the same date in the previous year using `SAMEPERIODLASTYEAR`.

---

## 11. Power BI Dashboard Specifications
The dashboard consists of 7 functional reporting views:
1. **Executive HR Overview**: Displays top-level KPI cards and department headcount distribution, providing a bird's-eye view of organizational health.
2. **Recruitment Analytics**: Displays the application funnel, average hire times, and recruitment channel performance.
3. **Employee Attrition Analysis**: Tracks attrition percentages across salary, role, tenure, and recruitment channels to isolate exit triggers.
4. **Performance & Satisfaction**: Features a quadrant scatter plot of satisfaction vs. performance, identifying high performers with low satisfaction.
5. **Workforce Demographics & Compensation**: Compares salaries across roles, departments, and genders, alongside geographic distributions.
6. **Hiring Forecast**: Visualizes historical monthly hiring counts alongside a 6-month predictive trend line.
7. **Insights & Recommendations**: Outlines strategic takeaways for leadership.

---

## 12. Recruitment Analytics Findings
Analysis of the recruitment pipeline shows that the candidate funnel has a conversion rate from application to hire of roughly **15%**. 
* **Recruitment Cost**: Executive Search represents the highest cost per hire (averaging ~\$18,000), but yields candidates with high interview scores.
* **Referrals**: Employee Referrals show the fastest average **Time to Hire** (approx. 22 days) and the lowest average sourcing cost (~\$650), while subsequently showing high retention rates.
* **Campus Sourcing**: College campus recruitment provides a high volume of junior candidates but exhibits a slower average onboarding time (Time to Hire ~48 days).

---

## 13. Attrition Analysis
Our findings show a clear picture of why employees leave:
* **Satisfaction Impact**: Employees with Satisfaction Scores of 1 or 2 represent **68%** of total exits.
* **Overtime Link**: Employees working more than 120 hours of overtime annually show an attrition rate of **32%**, significantly higher than the baseline average.
* **Department Hotspots**: Sales and Customer Service have the highest attrition rates (exceeding **20%**).
* **Compensation Gap**: Employees whose salaries fall in the bottom 25% percentile for their specific job role represent **45%** of all voluntary exits, highlighting salary compression issues.

---

## 14. Performance Analysis
The performance reviews dataset reveals:
* **Training Upskilling**: Employees who complete more than 60 hours of training annually average a performance rating of **4.1**, compared to **2.8** for those with less than 20 hours.
* **Manager Ratings**: There is a 90% correlation between subjective `Manager_Rating` and numerical `Goals_Achieved` (%), indicating that performance scores are aligned with output.
* **Promotions**: Promotions are highly concentrated in the IT and Finance departments, with Customer Service having the lowest internal promotion rate (less than 3% annually).

---

## 15. Satisfaction Analysis
Job satisfaction was mapped against operational and demographic variables:
* **Overtime and Workload**: Satisfaction drops significantly when overtime exceeds 100 hours annually, indicating burnout.
* **Absenteeism Correlation**: Employees with lower satisfaction scores (1 or 2) had an average of **12 days of absenteeism** per year, compared to only **3 days** for satisfied employees (score 4 or 5). This makes absenteeism a useful leading indicator of employee dissatisfaction.
* **Recruitment Source Impact**: Hires from 'Referrals' show the highest average satisfaction (4.2 out of 5), suggesting that cultural fit is stronger.

---

## 16. Hiring Forecast & Predictive Model
We built a trend-based forecasting model:
* **Algorithm**: Linear Regression.
* **Implementation**: Fits a line to historical monthly hires (Jan 2020 to Jun 2026).
* **Regression Equation**: `Monthly_Hires = -0.032 * Month_Index + 29.46`
* **Interpretation**: The slightly negative coefficient (-0.032) indicates that while overall company headcount is growing, the *rate* of new monthly hiring has slightly stabilized over the 6-year period.
* **Error Metrics**: Mean Absolute Error (MAE) of **4.60** hires per month, and Root Mean Squared Error (RMSE) of **5.79**.
* **6-Month Forecast**: Predicts a stable demand of **27 to 28** new hires per month for the upcoming 6 months (July to Dec 2026).

---

## 17. Key Findings Summary
1. **Workforce Stability**: The company has experienced stable hiring with a cumulative headcount growth, but attrition is concentrated in specific areas.
2. **Sales/CS Burnout**: Attrition in Sales and Customer Service is driven by a combination of high overtime, lower comparative salary, and low job satisfaction.
3. **Training ROI**: Internal training hours are strongly linked to higher performance scores and goals achieved.
4. **Referral Quality**: Employee referrals are the most cost-effective sourcing channel and produce employees with the highest satisfaction and retention rates.

---

## 18. Strategic Business Recommendations
Based on the data, we recommend the following actions:
1. **Overtime Caps**: Implement a policy limiting overtime to a maximum of 80 hours per employee per year in Sales and Customer Service to combat burnout.
2. **Referral Program Incentives**: Expand the Employee Referral Program. Reallocate 20% of the expensive Executive Search budget to referral bonuses, lowering overall recruitment costs while raising retention.
3. **Standard Training Hours**: Establish a minimum training threshold of 40 hours per year for all mid-level roles, given its clear positive correlation with performance.
4. **Targeted Compensation Reviews**: Conduct salary benchmarking for Sales and Customer Service roles, addressing the low salaries that are driving employee departures.

---

## 19. Project Limitations
* **Linear Model Simplicity**: The Python forecasting model uses simple linear regression, which captures long-term trends but does not account for monthly seasonal patterns (e.g. higher hiring in January and lower hiring in December).
* **Missing Macro-Indicators**: The datasets do not include external market conditions, such as competitor salaries, regional unemployment rates, or industry turnover averages.
* **No Qualitative Feedback**: Quantitative ratings (1-5) are used for satisfaction, but we lack text-based sentiment analysis from exit interviews or employee surveys.

---

## 20. Future Scope
* **Advanced Machine Learning**: In future iterations, models like XGBoost, Random Forest, or SARIMA could be implemented in Python to capture complex non-linear trends and seasonal hiring patterns.
* **NLP Sentiment Analysis**: Integrate exit interview comments and apply Natural Language Processing (NLP) to extract themes behind employee departures.
* **Real-time Pipeline Integration**: Connect Power BI directly to live HRIS and ATS databases using APIs, enabling real-time dashboard updates rather than batch CSV loads.

---

## 21. Conclusion
This HR Analytics project successfully demonstrates how integrating data cleaning, predictive modeling, and business intelligence can solve workforce management challenges. By cleaning and linking employees, recruitment, and performance data, we resolved key siloes. The analysis identified the root causes of employee attrition (overtime and satisfaction gaps), verified the value of training programs, evaluated recruitment channels, and forecasted future hiring requirements. Applying these insights will help the organization make strategic decisions that lower recruitment costs and improve employee retention.
