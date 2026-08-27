# Human Resources Analytics & Workforce Intelligence Dashboard

## Project Overview
This project is an end-to-end **HR Analytics & Workforce Intelligence** solution. It integrates data engineering (Python), machine learning (Scikit-Learn), and business intelligence (Power BI) to analyze and optimize employee demographics, recruitment, attrition, satisfaction, and performance. 

It provides an organization with historical context, real-time KPI monitoring, and a 6-month predictive forecast of future hiring requirements.

---

## 🚀 How I Can Explain This Project in an Interview (2-3 Minute Pitch)

*Use this simple, structured pitch to explain this project to recruiters or interviewers:*

> **"For my portfolio, I built a complete Human Resources Analytics and Workforce Intelligence Dashboard.**
>
> **The Problem:** 
> Many HR departments manage datasets in silos. They can track headcount but cannot identify what drives employee turnover, which hiring sources are most cost-effective, or how training impacts performance. They also hire reactively rather than planning ahead.
>
> **The Datasets:** 
> I generated and integrated three relational datasets: an **Employees** table (2,200 records), a **Recruitment** candidate pipeline (650 records), and a longitudinal **Performance** reviews table (5,954 records).
>
> **Data Cleaning:** 
> Using **Python (Pandas)**, I wrote a cleaning script to check for duplicates, verify referential integrity, and resolve logical conflicts (such as verifying experience matched age, and ensuring exit dates were only populated for former employees).
>
> **Power BI Modeling & DAX:** 
> I imported the clean data into Power BI and designed a **Star Schema** data model. I created a custom DAX **Calendar table** to link all date columns. I then wrote over **20 DAX measures** (like Attrition Rate, Hiring Rate, and YoY Employee Growth) to dynamically aggregate KPIs.
>
> **The Dashboard:** 
> I built a 7-page interactive report covering an **Executive Overview**, **Recruitment Analytics**, **Attrition Analysis**, **Performance & Satisfaction**, **Workforce Demographics**, a **Hiring Forecast**, and a **Management Insights** slide deck.
>
> **Predictive Analytics:** 
> To project future hiring needs, I built a **Linear Regression model in Python**. The model aggregated historical hires monthly, calculated performance metrics (MAE: 4.60, RMSE: 5.79), and projected a steady demand of **27 to 28 hires per month** for the next 6 months.
>
> **Key Insights & Business Impact:** 
> My analysis revealed that **excessive overtime (>120 hours)** and **low satisfaction** are the main triggers for attrition, particularly in Sales and Customer Service. Furthermore, **Employee Referrals** were the most cost-effective channel (averaging $650 per hire) and produced the highest retention rates.
>
> **My Recommendations:** 
> I proposed capping overtime to prevent burnout, shifting 20% of the expensive executive search budget into referral bonuses, and establishing a minimum 40-hour training target, since training showed a direct positive correlation with performance ratings."*

---

## 📂 Project Directory Structure
```text
HR_Analytics_Project/
│
├── data/
│   ├── employees.csv              # Main employee records (2,200 rows)
│   ├── recruitment.csv            # Candidate tracking pipeline (650 rows)
│   ├── performance.csv            # Employee review cycles (5,954 rows)
│   └── hiring_forecast_output.csv # 6-month forecast output (Python generated)
│
├── python/
│   ├── data_generation.py         # Synthetic data generation script
│   ├── data_cleaning.py           # Integrity checks and data quality validation
│   └── hiring_forecast.py         # Linear regression predictive analytics model
│
├── powerbi/
│   ├── DAX_Measures.dax           # Reference catalog of all DAX measures
│   └── HR_Dashboard_Build_Guide.md # Step-by-step layout & theme build guide
│
└── documentation/
    ├── Data_Quality_Report.md     # Logs from data cleaning execution
    ├── Data_Dictionary.md         # Schema descriptions for all columns
    ├── Forecasting_Model_Details.md # Details about regression scores & assumptions
    ├── Project_Report.md          # College/internship academic project report
    └── Viva_Questions.md          # 32 Viva preparation Q&As for freshers
```

---

## 🛠️ Tools & Technologies Used
* **Data Engineering**: Python 3, Pandas, NumPy
* **Predictive Analytics (ML)**: Python Scikit-Learn (Linear Regression)
* **Visualization Plotting**: Matplotlib
* **Business Intelligence (BI)**: Power BI Desktop (Power Query, DAX, Star Schema Modeling)
* **Documentation**: Markdown, Mermaid.js (for ER diagrams)

---

## 📊 Data Model (Star Schema)
The Power BI model is optimized in a star schema:
* **Facts**: `Fact_Employees`, `Fact_Recruitment`, `Fact_Performance`
* **Dimensions**: `Dim_Date` (Calendar dimension table created using DAX)
* **Forecasting**: `Fact_HiringForecast`

Relationships are established using a **1-to-many (1:\*)** structure flowing from `Dim_Date` to all chronological columns.

---

## 📈 Key Metrics & DAX Measures
Over 20 measures are pre-written and documented in [powerbi/DAX_Measures.dax](file:///c:/Users/Newman/Documents/HR_Analytics_Project/powerbi/DAX_Measures.dax), including:
* **Total Employees** = `COUNTROWS(Fact_Employees)`
* **Active Employees** = `CALCULATE([Total Employees], Fact_Employees[Employment_Status] = "Active")`
* **Attrition Rate** = `DIVIDE([Employees Left], [Total Employees], 0)`
* **Retention Rate** = `1 - [Attrition Rate]`
* **Average Time to Hire** = `AVERAGE(Fact_Recruitment[Time_to_Hire])`
* **Hiring Rate** = `DIVIDE([Total Joined], [Total Applications], 0)`

---

## 📑 Dashboard Pages Summary
1. **Executive HR Overview**: High-level corporate health KPIs, headcount by department, and attrition rates.
2. **Recruitment Analytics**: Conversion funnels, recruitment source costs, and time-to-hire metrics.
3. **Employee Attrition Analysis**: Deep-dive on departures segmented by salary brackets, roles, gender, and overtime hours.
4. **Performance & Satisfaction**: Interaction grids showing upskilling impact (training hours) and manager ratings.
5. **Workforce Demographics & Compensation**: Geographical mapping, age distributions, and salary equity by department.
6. **Hiring Forecast**: Interactive time-series trends comparing actual hiring numbers with a 6-month prediction model.
7. **Insights & Recommendations**: Presentation layout containing clear strategic directions for business decision-makers.

---

## 🏃 How to Run the Project

### Step 1: Run the Python Data Pipeline
Ensure you have the required libraries installed:
```powershell
pip install pandas numpy scikit-learn matplotlib
```
Execute the scripts in order:
1. **Generate Data**: `python python/data_generation.py`
2. **Clean & Validate**: `python python/data_cleaning.py`
3. **Predict Forecast**: `python python/hiring_forecast.py`

### Step 2: Build the Power BI Dashboard
1. Open **Power BI Desktop**.
2. Import the CSV files from the `data/` folder.
3. Apply the schema connections and DAX measures as detailed in the [Power BI Build Guide](file:///c:/Users/Newman/Documents/HR_Analytics_Project/powerbi/HR_Dashboard_Build_Guide.md).
4. Build the visuals on each page following the provided layout coordinates.

---

## 🔮 Future Improvements
* **Advanced Machine Learning**: Implement time-series algorithms (like **SARIMA** or **Prophet**) to capture seasonality (e.g. December hiring freezes).
* **Sentiment Analysis**: Integrate text analytics for employee exit surveys.
* **Direct database integration**: Connect live database connections using API pipelines.
