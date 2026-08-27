# Internship Submission Summary & Portfolio Guide

This document contains the official project summary, portfolio showcase guide, and social media post templates for the **HR Analytics & Workforce Intelligence** project.

---

## 1. Professional Project Summary (For Submission)
*Copy and paste this into your internship report, college project portal, or evaluation document:*

### Project Metadata
* **Title**: Human Resources Analytics & Workforce Intelligence Dashboard
* **Objective**: To design and build an end-to-end People Analytics solution that integrates HRIS data (employees), ATS data (recruitment), and PMS data (performance reviews) to analyze attrition patterns, evaluate recruitment channels, and forecast 6-month hiring headcount.
* **Technology Stack**: Python (Pandas, NumPy, Scikit-Learn for forecasting), Power BI Desktop (Power Query, DAX, Star Schema Modeling), and Git.

### Executive Summary
The organization faced challenges with rising attrition rates in key departments (Sales and Customer Service), unmeasured recruitment channel budgets, and a lack of predictive foresight for future staffing needs. 

To address this, we developed a three-stage analytics pipeline:
1. **Data Engineering (Python)**: Loaded and cleaned 2,200 employee rows, 650 recruitment applications, and 5,954 performance records. The cleaning script verified age/experience consistency, mapped active/former employee flags, and checked referential integrity.
2. **Predictive Modeling (Scikit-Learn)**: Aggregated monthly hiring numbers and trained a Linear Regression model. The model fitted a trend line (`Hires = -0.032 * Month_Index + 29.46`) with a Mean Absolute Error (MAE) of 4.60 hires, predicting a steady hiring requirement of **27 to 28 hires per month** for the next 6 months.
3. **Business Intelligence (Power BI)**: Configured a relational Star Schema linking all datasets to a central date table (`Dim_Date`). Developed 22 DAX measures to track KPIs dynamically, and built a 7-page interactive report with drill-through detail views.

### Key Insights & Impact
* **Attrition Drivers**: Identified that 68% of departures were driven by low job satisfaction, strongly correlated with high overtime hours (>120 hours annually) and lower comparative salaries.
* **Sourcing ROI**: Discovered that **Employee Referrals** are the most cost-effective channel (averaging \$650 per hire) and produce candidates with the highest retention rates.
* **Training Value**: Validated that employees with >60 hours of training score an average of 4.1 in performance (compared to 2.8 for <20 hours).
* **Strategic Actions**: Caps on overtime, expanding referral bonuses, and setting up mandatory training thresholds will reduce recruitment costs and improve employee retention.

---

## 2. Screenshot Checklist (Proof of Work)
When you build the Power BI dashboard, take the following screenshots as proof of completion for your project report:

1. **Screenshot 1: The Data Model (Star Schema)**  
   * **Where**: Go to the **Model View** in Power BI Desktop (third icon on the left sidebar).
   * **Details**: Adjust the tables (`Dim_Date`, `Fact_Employees`, `Fact_Recruitment`, `Fact_Performance`, `Fact_HiringForecast`) on the screen so all relationship lines and keys are clearly visible. Capture the complete diagram.
2. **Screenshot 2: Executive Overview Dashboard Page**  
   * **Where**: Go to the **Report View** > Page 1 (Executive HR Overview).
   * **Details**: Ensure the KPI cards (2,200 employees, 12.00% attrition rate, etc.) and charts are fully populated. Highlight the clean corporate theme.
3. **Screenshot 3: Recruitment Funnel & Sourcing Analytics**  
   * **Where**: Go to Page 2 (Recruitment & Hiring).
   * **Details**: Highlight the Funnel visual showing conversion stages from "Applied" to "Joined" alongside the cost-per-hire bar chart.
4. **Screenshot 4: Employee Attrition & Overtime Scatter Plot**  
   * **Where**: Go to Page 3 (Employee Attrition Analysis).
   * **Details**: Capture the attrition rate segmented by salary brackets and job roles.
5. **Screenshot 5: Employee Performance Quadrant Plot**  
   * **Where**: Go to Page 4 (Performance & Satisfaction).
   * **Details**: Highlight the Scatter Plot showing the four performance vs. satisfaction quadrants with the constant reference lines.
6. **Screenshot 6: 6-Month Hiring Forecast Timeline**  
   * **Where**: Go to Page 6 (Hiring Forecast).
   * **Details**: Show the line chart plotting historical hires alongside the green dashed forecast line.
7. **Screenshot 7: Python Forecasting Pipeline Run**  
   * **Where**: Run `python python/hiring_forecast.py` in your terminal.
   * **Details**: Screenshot the command line output displaying the MAE, RMSE, and the regression formula as proof of your data science code running successfully.

---

## 3. Professional LinkedIn / GitHub Post Description
*Use this text to showcase your completed project on LinkedIn or in your GitHub repository:*

```text
🎉 Project Complete: HR Analytics & Workforce Intelligence Dashboard!

I have just completed an end-to-end People Analytics project designed to help organizations make data-backed workforce decisions. 

Here is a summary of what I built:
1️⃣ Data Pipeline (Python/Pandas): Preprocessed and validated three relational tables (2.2k employees, 650 applicant pipelines, and 5.9k review records) ensuring 100% data integrity.
2️⃣ Predictive Modeling (Scikit-Learn): Trained a Linear Regression model on historical monthly hires to forecast recruitment headcount demands for the next 6 months (Model MAE: 4.60).
3️⃣ Star-Schema Modeling (Power BI): Modeled relationships connecting all facts to a central DAX Calendar table to avoid many-to-many conflicts.
4️⃣ Metric Engineering (DAX): Developed 20+ measures including Attrition Rate, Retention Rate, Time-to-Hire, and YoY Headcount Growth.
5️⃣ Dashboard Interface: Built a 7-page interactive dashboard detailing Executive Overview, Recruitment Funnel, Attrition Triggers, Compensation Equity, and Actionable Management Recommendations.

💡 Core Business Takeaways:
- Employee Referrals represent the highest ROI sourcing channel (lowest cost of $650/hire, highest subsequent satisfaction and retention).
- High attrition (Sales/Customer Service) is heavily driven by excessive overtime (>120 hours/year).
- Mandatory training hours (>40h/year) directly correlate with higher performance ratings (4.1/5.0 vs 2.8/5.0).

This project has been added to my portfolio, demonstrating my skills in Data Engineering, Machine Learning, and Business Intelligence!

#HRAnalytics #PeopleAnalytics #PowerBI #Python #DataScience #DataAnalytics #InternshipProject #Portfolio
```
