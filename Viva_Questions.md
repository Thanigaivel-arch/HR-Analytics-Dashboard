# Viva / Interview Preparation Questions & Answers

This guide contains **32 questions and answers** to help freshers and beginners explain this HR Analytics project during a college viva, project defense, or job interview. The answers are designed to be simple, technically accurate, and easy to explain in plain English.

---

## Part 1: Power BI & Data Modeling Concepts

### Q1: Why did you choose Power BI for this project instead of Excel?
**Answer:** While Excel is great for basic data entry and static tables, Power BI is designed specifically for Business Intelligence. It handles large datasets efficiently, allows us to build a relational database model (star schema), supports interactive filtering (slicers), and lets us build dynamic, automated dashboards that can refresh when new data is added.

### Q2: What is Power Query, and how did you use it in this project?
**Answer:** Power Query is the data transformation and ETL (Extract, Transform, Load) engine in Power BI. We used it to import our CSV files, verify that the columns had the correct data types (e.g. converting date columns, setting salary to currency), promote headers, and load the clean tables into the Power BI data model.

### Q3: What is DAX?
**Answer:** DAX stands for **Data Analysis Expressions**. It is the formula language used in Power BI to create custom calculations, aggregations, and metrics. We used DAX to calculate KPIs like `Attrition Rate`, `Active Headcount`, and time-intelligence growth metrics.

### Q4: What is a Measure in Power BI?
**Answer:** A measure is a dynamic calculation in Power BI. It does not occupy space in the database; instead, it is calculated on the fly (in real time) based on the filters or slicers selected on the dashboard page. For example, our `Attrition Rate` is a measure.

### Q5: What is the difference between a Calculated Column and a Measure?
**Answer:** 
* **Calculated Column**: Computes values row-by-row and stores them in the table, increasing the file size. Use it when you need to slice or group data (e.g., creating a "Salary Group" bucket).
* **Measure**: Computed on the fly when you interact with the dashboard. It does not increase file size and changes dynamically based on dashboard filters.

### Q6: What is a Star Schema, and why did you use it?
**Answer:** A Star Schema is a data modeling design where a central Fact table is surrounded by and linked to several Dimension tables. It looks like a star. We used it because it is the industry best-practice for Power BI. It simplifies our DAX calculations, prevents many-to-many relationship errors, and makes dashboards run faster.

### Q7: What are Fact tables and Dimension tables in your project?
**Answer:**
* **Fact Tables**: Contain quantitative data or measurements (numerical transactions). In our project, `Fact_Employees`, `Fact_Recruitment`, and `Fact_Performance` are fact tables.
* **Dimension Tables**: Contain descriptive context or attributes. `Dim_Date` (Calendar) is our dimension table, which links the other tables together.

### Q8: What are the relationships in your data model?
**Answer:** We established 1-to-many (1:\*) relationships from our `Dim_Date` table to the date columns in our fact tables. For example, `Dim_Date[Date]` links to `Fact_Employees[Joining_Date]` and `Fact_Performance[Review_Date]`.

### Q9: Why do you have active and inactive relationships in your model?
**Answer:** In Power BI, you can only have *one* active relationship between two tables at a time. In our `Fact_Employees` table, we have two date columns: `Joining_Date` and `Exit_Date`. We made the relationship with `Joining_Date` active (default) and the relationship with `Exit_Date` inactive. If we need to calculate metrics using `Exit_Date`, we use the DAX function `USERELATIONSHIP()` to temporarily activate it.

### Q10: What is Cross-Filtering?
**Answer:** Cross-filtering is the default behavior in Power BI where selecting a data point in one chart automatically filters all other charts on the same dashboard page. For example, clicking on the "IT" department bar automatically updates the Attrition and Gender charts to show IT-only data.

### Q11: What is Drill-Down in Power BI?
**Answer:** Drill-down is a feature that allows users to navigate from a high-level summary to a more detailed view within the same visual. For example, in our monthly hiring line chart, a user can click drill-down to view hiring numbers by quarter, and then drill down further to see monthly or daily numbers.

### Q12: What are Slicers?
**Answer:** Slicers are visual filters placed directly on the dashboard canvas (usually as dropdowns or buttons). They allow users to quickly filter the entire page by variables like Year, Department, Location, or Job Role.

---

## Part 2: HR Domain & Project Business Metrics

### Q13: What business problem does this project solve?
**Answer:** This project helps organizational leadership move from guesswork to data-backed decisions. It solves four main problems: identifying what drives employee attrition, measuring which recruitment sources are most cost-effective, analyzing the impact of training on performance, and forecasting monthly hiring needs to avoid staffing shortages.

### Q14: What is Attrition, and how is Attrition Rate calculated?
**Answer:** Attrition refers to the voluntary or involuntary departure of employees from an organization. In our dashboard, the Attrition Rate measure is calculated using the DAX formula:
$$\text{Attrition Rate} = \frac{\text{Employees Left}}{\text{Total Headcount}}$$
This represents the percentage of cumulative employees who have exited.

### Q15: What is the difference between Attrition Rate and Retention Rate?
**Answer:** Attrition Rate measures the percentage of employees who left the company, while Retention Rate measures the percentage of employees who stayed. They are opposites, meaning:
$$\text{Retention Rate} = 1 - \text{Attrition Rate}$$

### Q16: What is Time to Hire, and why does it matter?
**Answer:** Time to Hire is the number of days between a candidate submitting their application and the date they are hired. It is an efficiency metric. A long Time to Hire indicates bottlenecks in the recruitment process, which can lead to losing top candidates to competitors.

### Q17: What is Recruitment Cost, and how do you analyze it?
**Answer:** Recruitment Cost is the financial expense incurred to hire a new employee. In our project, we analyze it by **Recruitment Source** (e.g. LinkedIn, Referrals, Executive Search). This helps HR identify which sourcing channels give the best value (low cost-per-hire with high-performing candidates).

### Q18: What is Absenteeism, and how does it relate to employee satisfaction?
**Answer:** Absenteeism is the number of days an employee is absent from work (due to sickness or unexplained reasons). Our analysis revealed that dissatisfied employees (satisfaction scores of 1 or 2) had significantly higher absenteeism rates, making it a key early indicator of burnout or low morale.

### Q19: What is Overtime, and what impact does it have on attrition?
**Answer:** Overtime is the number of hours worked beyond standard hours. Our analysis shows a strong correlation where employees with high overtime (>120 hours annually) had an attrition rate of **32%**, indicating that excessive workloads are a major driver of turnover.

---

## Part 3: Python Analytics & Machine Learning Forecasting

### Q20: Why did you use Python in this project?
**Answer:** Python was used for three key tasks: 
1. **Data Generation**: Creating a realistic relational database.
2. **Data Cleaning**: Running automated validation checks.
3. **Predictive Analytics**: Building a machine learning forecasting model to predict future hiring requirements.

### Q21: What machine learning algorithm did you use for the forecast, and why?
**Answer:** We used **Linear Regression** (using `scikit-learn`). We chose it because it is simple, highly explainable, and ideal for a junior portfolio. It captures the long-term hiring growth trend line, making it easy to explain to stakeholders.

### Q22: What were the input and output variables of your forecasting model?
**Answer:**
* **Input variable (Independent feature)**: `Month_Index` (A sequential timeline index: 1, 2, 3... representing consecutive months from January 2020 onwards).
* **Output variable (Dependent target)**: `Hires` (The total number of employees hired in that month).

### Q23: What does the regression formula `Hires = -0.032 * Month_Index + 29.46` mean?
**Answer:** 
* The **intercept (29.46)** represents the baseline number of monthly hires at the start of our timeline.
* The **slope (-0.032)** represents the monthly change. The negative sign shows that while the company is growing, the *monthly rate* of hiring has slightly stabilized over time.

### Q24: What is MAE, and what was your model's MAE?
**Answer:** MAE stands for **Mean Absolute Error**. It measures the average magnitude of errors in a set of predictions. Our model's MAE is **4.60**, meaning that on average, our model's predictions deviate from the actual hiring data by about 4.6 hires per month.

### Q25: What is RMSE, and why is it useful?
**Answer:** RMSE stands for **Root Mean Squared Error**. It is another error metric. Unlike MAE, RMSE penalizes larger errors more heavily because it squares the errors before averaging them. Our model's RMSE is **5.79**.

### Q26: What are the limitations of your Linear Regression forecasting model?
**Answer:** The main limitation is that a simple linear trend cannot capture monthly seasonality (for example, peak hiring periods after college graduation, or hiring freezes in December). In the future, a time-series model like **SARIMA** could be used to capture seasonal patterns.

### Q27: Is your hiring forecast guaranteed to be correct?
**Answer:** No. Machine learning forecasts are estimates based on historical patterns. They cannot predict unexpected changes like company budget cuts, mergers, or sudden economic recessions. They should be used as a strategic planning guide, not a guarantee.

---

## Part 4: Key Insights & Project Value

### Q28: What is the most important insight you derived from the data?
**Answer:** The most critical insight is the root cause of employee attrition. We found that low job satisfaction (scores of 1 or 2) and high overtime (>120 hours) are the strongest predictors of departures. Attrition is heavily concentrated in Sales and Customer Service, which correlates with high overtime workloads.

### Q29: What is your recommendation for reducing recruitment costs?
**Answer:** Our data shows that **Employee Referrals** are highly cost-effective (averaging \$650 per hire) and produce candidates with high job satisfaction and low attrition. I recommend shifting 20% of the expensive Executive Search budget into referral bonuses to drive referral volume.

### Q30: How does training affect employee performance in this organization?
**Answer:** There is a clear positive correlation: employees who completed more than 60 hours of training had an average performance rating of **4.1**, compared to just **2.8** for those with under 20 hours of training. This proves that training budgets are yielding a positive return on investment (ROI).

### Q31: How can an HR Manager use this dashboard?
**Answer:** An HR Manager can use it to:
1. Spot departments with high attrition and step in with retention programs.
2. Monitor recruitment costs and adjust sourcing budgets.
3. Review training completion rates and performance ratings.
4. View the 6-month hiring forecast to allocate recruitment staff and plan upcoming budgets.

### Q32: If you had more time, how would you improve this project?
**Answer:** I would add:
1. **Natural Language Processing (NLP)** to analyze written exit interview feedback.
2. An advanced forecasting model like **XGBoost** to capture seasonal patterns.
3. A live database connection (using APIs) so the dashboard updates automatically.
