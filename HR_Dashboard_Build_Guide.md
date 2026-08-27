# Complete Power BI Build Guide: HR Analytics & Workforce Intelligence

This document is a comprehensive, step-by-step manual designed to help a beginner build the entire **Human Resources Analytics & Workforce Intelligence Dashboard** from scratch in **Power BI Desktop**. 

All data cleaning, modeling, DAX measures, visuals, and configurations are customized to the actual datasets generated in your workspace.

---

## 1. CSV Files to Import
You need to import the four CSV datasets located in your `HR_Analytics_Project/data/` folder:
1. `employees.csv` (Main workforce profiles)
2. `recruitment.csv` (Candidate pipeline history)
3. `performance.csv` (Periodic review ratings)
4. `hiring_forecast_output.csv` (Python regression model outputs)

---

## 2. Power Query Data-Cleaning & Transformations
Follow these exact steps in **Power Query Editor** to clean and prepare your data:

### Launching Power Query:
1. Open **Power BI Desktop**.
2. Click **Get Data** > **Text/CSV** > Select `employees.csv` > Click **Transform Data** (not Load).
3. In the left panel (Queries), right-click and select **New Query** > **File** > **CSV** to add the remaining three files: `recruitment.csv`, `performance.csv`, and `hiring_forecast_output.csv`.
4. Rename the queries in the **Properties** panel on the right:
   * Rename `employees` to **`Fact_Employees`**
   * Rename `recruitment` to **`Fact_Recruitment`**
   * Rename `performance` to **`Fact_Performance`**
   * Rename `hiring_forecast_output` to **`Fact_HiringForecast`**

### Query 1: Fact_Employees Cleaning
* **Remove Duplicates**: Right-click the `Employee_ID` column header > Select **Remove Duplicates** (guarantees ID uniqueness).
* **Data Types**: Change data types by clicking the type icon next to column headers:
  * `Employee_ID`, `Employee_Name`, `Gender`, `Department`, `Job_Role`, `Education`, `Recruitment_Source`, `Location`: **Text**
  * `Age`, `Experience_Years`, `Training_Hours`, `Absenteeism_Days`, `Overtime_Hours`: **Whole Number**
  * `Performance_Score`, `Satisfaction_Score`: **Whole Number**
  * `Joining_Date`, `Exit_Date`: **Date**
  * `Salary`: **Fixed Decimal Number** (Currency)
  * `Employment_Status`: **Text**
* **Handle Null Exit Dates**: Power Query automatically replaces blank cells in `Exit_Date` with `null`. Keep this as-is; it is the correct way for Power BI to handle active employees.

### Query 2: Fact_Recruitment Cleaning
* **Remove Duplicates**: Right-click the `Candidate_ID` column header > Select **Remove Duplicates**.
* **Data Types**:
  * `Candidate_ID`, `Department`, `Job_Role`, `Recruitment_Source`, `Candidate_Status`: **Text**
  * `Application_Date`, `Hiring_Date`: **Date** (blanks in `Hiring_Date` are loaded as `null` for rejected/in-progress applicants).
  * `Interview_Score`, `Experience_Years`, `Time_to_Hire`: **Whole Number** (If `Time_to_Hire` has blanks, load them as `null`).
  * `Expected_Salary`, `Offered_Salary`, `Recruitment_Cost`: **Fixed Decimal Number** (Currency)

### Query 3: Fact_Performance Cleaning
* **Remove Duplicate Review Rows**: Select both `Employee_ID` and `Review_Date` columns > Right-click > Select **Remove Duplicates** (ensures each employee only has one review recorded on any single date).
* **Data Types**:
  * `Employee_ID`, `Promotion_Status`: **Text**
  * `Review_Date`: **Date**
  * `Performance_Score`, `Satisfaction_Score`, `Training_Hours`, `Goals_Achieved`, `Manager_Rating`: **Whole Number**

### Query 4: Fact_HiringForecast Cleaning
* **Data Types**:
  * `Date`: **Date**
  * `Historical_Hires`, `Forecasted_Hires`: **Whole Number**
  * `Type`: **Text**

*After completing these steps, click **Close & Apply** on the Home tab ribbon.*

---

## 3. Data Model Architecture (Star Schema)
To create a high-performance model, go to the **Model View** (left-most sidebar) and set up the relationships:

### Step 1: Create the DAX Calendar Table
1. In the Modeling tab at the top of the main window, click **New Table**.
2. Paste the following formula:
```dax
Dim_Date = 
VAR MinDate = MIN(Fact_Employees[Joining_Date])
VAR MaxDate = DATE(2026, 12, 31) // Cover the 6-month forecast window
RETURN
ADDCOLUMNS(
    CALENDAR(MinDate, MaxDate),
    "Year", YEAR([Date]),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "Month Number", MONTH([Date]),
    "Month Name", FORMAT([Date], "MMMM"),
    "Month Short", FORMAT([Date], "MMM"),
    "Year Month", FORMAT([Date], "YYYY-MM"),
    "Day of Week", FORMAT([Date], "dddd")
)
```
3. Right-click the newly created `Dim_Date` table > Click **Mark as Date Table** > Select the `Date` column > Click **OK**.

### Step 2: Establish Relationships
Drag and drop fields to link tables. Configure settings exactly as follows:

| From Table (Dimension) | From Field | To Table (Fact) | To Field | Cardinality | Cross Filter Direction | Relationship Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Dim_Date** | `Date` | `Fact_Employees` | `Joining_Date` | 1-to-many (1:\*) | Single (Dim filters Fact) | **Active** |
| **Dim_Date** | `Date` | `Fact_Employees` | `Exit_Date` | 1-to-many (1:\*) | Single (Dim filters Fact) | **Inactive** |
| **Dim_Date** | `Date` | `Fact_Recruitment` | `Application_Date` | 1-to-many (1:\*) | Single (Dim filters Fact) | **Active** |
| **Dim_Date** | `Date` | `Fact_Recruitment` | `Hiring_Date` | 1-to-many (1:\*) | Single (Dim filters Fact) | **Inactive** |
| **Dim_Date** | `Date` | `Fact_Performance` | `Review_Date` | 1-to-many (1:\*) | Single (Dim filters Fact) | **Active** |
| **Dim_Date** | `Date` | `Fact_HiringForecast` | `Date` | 1-to-many (1:\*) | Single (Dim filters Fact) | **Active** |
| **Fact_Employees** | `Employee_ID` | `Fact_Performance` | `Employee_ID` | 1-to-many (1:\*) | Single (Emp filters Perf) | **Active** |

---

## 4. Copy-Paste DAX Measures
Create a dedicated table to house your measures:
1. In the Home tab, click **Enter Data**.
2. Name the table **`_Measures`** and click **Load**.
3. Create the following measures one-by-one by clicking **New Measure** in the Modeling tab:

```dax
// 1. Total Employees
Total Employees = COUNTROWS(Fact_Employees)
```

```dax
// 2. Active Employees
Active Employees = CALCULATE([Total Employees], Fact_Employees[Employment_Status] = "Active")
```

```dax
// 3. Employees Left
Employees Left = CALCULATE([Total Employees], Fact_Employees[Employment_Status] = "Left")
```

```dax
// 4. Attrition Rate
Attrition Rate = DIVIDE([Employees Left], [Total Employees], 0)
```

```dax
// 5. Retention Rate
Retention Rate = 1 - [Attrition Rate]
```

```dax
// 6. Average Salary
Average Salary = AVERAGE(Fact_Employees[Salary])
```

```dax
// 7. Total Salary Expense
Total Salary Expense = SUM(Fact_Employees[Salary])
```

```dax
// 8. Average Satisfaction
Average Satisfaction = AVERAGE(Fact_Employees[Satisfaction_Score])
```

```dax
// 9. Average Performance
Average Performance = AVERAGE(Fact_Employees[Performance_Score])
```

```dax
// 10. Average Training Hours
Average Training Hours = AVERAGE(Fact_Employees[Training_Hours])
```

```dax
// 11. Average Absenteeism
Average Absenteeism = AVERAGE(Fact_Employees[Absenteeism_Days])
```

```dax
// 12. Average Overtime
Average Overtime = AVERAGE(Fact_Employees[Overtime_Hours])
```

```dax
// 13. Total Applications
Total Applications = COUNTROWS(Fact_Recruitment)
```

```dax
// 14. Total Selected
Total Selected = CALCULATE(COUNTROWS(Fact_Recruitment), Fact_Recruitment[Candidate_Status] IN { "Selected", "Joined" })
```

```dax
// 15. Total Joined (Hires)
Total Joined = CALCULATE(COUNTROWS(Fact_Recruitment), Fact_Recruitment[Candidate_Status] = "Joined")
```

```dax
// 16. Hiring Rate
Hiring Rate = DIVIDE([Total Joined], [Total Applications], 0)
```

```dax
// 17. Average Time to Hire
Average Time to Hire = AVERAGE(Fact_Recruitment[Time_to_Hire])
```

```dax
// 18. Average Recruitment Cost
Average Recruitment Cost = AVERAGE(Fact_Recruitment[Recruitment_Cost])
```

```dax
// 19. Net Headcount Growth
Employee Growth = [Total Joined] - CALCULATE([Employees Left], USERELATIONSHIP(Fact_Employees[Exit_Date], Dim_Date[Date]))
```

```dax
// 20. YoY Employee Growth Rate
YoY Employee Growth = 
VAR CurrentHeadcount = [Active Employees]
VAR LastYearHeadcount = CALCULATE([Active Employees], SAMEPERIODLASTYEAR(Dim_Date[Date]))
RETURN 
IF(ISBLANK(LastYearHeadcount) || LastYearHeadcount = 0, BLANK(), DIVIDE(CurrentHeadcount - LastYearHeadcount, LastYearHeadcount, 0))
```

```dax
// 21. High Performance Rate (%)
Performance Rate = DIVIDE(CALCULATE([Total Employees], Fact_Employees[Performance_Score] >= 4), [Total Employees], 0)
```

```dax
// 22. High Satisfaction Rate (%)
Satisfaction Rate = DIVIDE(CALCULATE([Total Employees], Fact_Employees[Satisfaction_Score] >= 4), [Total Employees], 0)
```

*After creating these, right-click the empty column "Column1" in the `_Measures` table and click **Delete** so only the measures are displayed with a small calculator icon.*

---

## 5. Dashboard Layout & Design Guide
* **Grid Layout**: Set page sizes to 16:9 widescreen.
* **Colors**: 
  * Primary Theme Dark: `#1D3557` (Navy Blue)
  * Secondary Highlights: `#457B9D` (Steel Blue)
  * Success/Target: `#2A9D8F` (Teal)
  * Warning/Danger: `#E76F51` (Coral/Peach)
  * Card Backgrounds: White (`#FFFFFF`) with 5px rounded corners and a soft shadow.
* **Typography**: Segoe UI. Use size 24 for page titles, 10 for visual headers (bold), and 9 for data labels.

---

## 6. Page-by-Page Visual Construction

### PAGE 1: EXECUTIVE HR OVERVIEW
* **Slicers** (Format: Dropdown or Tiles):
  * `Dim_Date[Year]`
  * `Fact_Employees[Department]`
  * `Fact_Employees[Location]`
* **KPI Card Visuals** (Arrange in a top horizontal row):
  * Card 1: Field = `[Total Employees]`
  * Card 2: Field = `[Active Employees]`
  * Card 3: Field = `[Employees Left]`
  * Card 4: Field = `[Attrition Rate]` (Format as %)
  * Card 5: Field = `[Average Salary]` (Format as Currency, 0 decimals)
  * Card 6: Field = `[Average Satisfaction]` (Format as Decimal, 1 decimal place)
* **Visuals**:
  1. **Stacked Bar Chart**: "Workforce by Department"
     * Y-Axis: `Fact_Employees[Department]`
     * X-Axis: `[Total Employees]`
  2. **Clustered Column Chart**: "Attrition Rate by Department"
     * X-Axis: `Fact_Employees[Department]`
     * Y-Axis: `[Attrition Rate]`
  3. **Line Chart**: "Headcount Hiring Trends"
     * X-Axis: `Dim_Date[Year Month]`
     * Y-Axis: `[Total Employees]`
  4. **Donut Chart**: "Diversity Representation"
     * Legend: `Fact_Employees[Gender]`
     * Values: `[Total Employees]`
  5. **Column Chart**: "Workforce Age Profile"
     * Grouping: Drag `Fact_Employees[Age]` into a new group (Right-click `Age` > **New Group** > Bin size 10) and drop to X-Axis.
     * Y-Axis: `[Total Employees]`

---

### PAGE 2: RECRUITMENT & HIRING ANALYTICS
* **Slicers**:
  * `Fact_Recruitment[Recruitment_Source]`
  * `Fact_Recruitment[Department]`
* **KPI Cards**:
  * `[Total Applications]`, `[Total Selected]`, `[Total Joined]`, `[Hiring Rate]`, `[Average Time to Hire]` (suffix "days"), `[Average Recruitment Cost]` (Format as Currency)
* **Visuals**:
  1. **Funnel Chart**: "Candidate Conversion Pipeline"
     * Group: `Fact_Recruitment[Candidate_Status]`
     * Values: `[Total Applications]`
  2. **Line Chart**: "Monthly Applications & Joining Trend"
     * X-Axis: `Dim_Date[Year Month]`
     * Y-Axis: `[Total Applications]` and `[Total Joined]`
  3. **Clustered Column Chart**: "Average Time to Hire by Department"
     * X-Axis: `Fact_Recruitment[Department]`
     * Y-Axis: `[Average Time to Hire]`
  4. **Horizontal Bar Chart**: "Average Cost by Sourcing Channel"
     * Y-Axis: `Fact_Recruitment[Recruitment_Source]`
     * X-Axis: `[Average Recruitment Cost]`
  5. **Table**: "Sourcing Performance Metrics"
     * Columns: `Fact_Recruitment[Recruitment_Source]`, `[Total Applications]`, `[Hiring Rate]`, `[Average Time to Hire]`, `[Average Recruitment Cost]`

---

### PAGE 3: EMPLOYEE ATTRITION ANALYSIS
* **KPI Cards**:
  * `[Attrition Rate]`, `[Employees Left]`, `[Retention Rate]`
* **Visuals**:
  1. **Column Chart**: "Attrition Rate by Salary Bracket"
     * *First, create a calculated column in `Fact_Employees`*:
       ```dax
       Salary Bracket = 
       IF(Fact_Employees[Salary] < 50000, "Under $50k", 
       IF(Fact_Employees[Salary] <= 90000, "$50k - $90k", 
       IF(Fact_Employees[Salary] <= 130000, "$90k - $130k", "Above $130k")))
       ```
     * X-Axis: `Fact_Employees[Salary Bracket]`
     * Y-Axis: `[Attrition Rate]`
  2. **100% Stacked Column Chart**: "Attrition Ratio by Gender"
     * X-Axis: `Fact_Employees[Gender]`
     * Legend: `Fact_Employees[Employment_Status]`
     * Y-Axis: `[Total Employees]`
  3. **Bar Chart**: "Top Roles by Attrition Rate"
     * Y-Axis: `Fact_Employees[Job_Role]`
     * X-Axis: `[Attrition Rate]` (Filter top 10 using Filter Pane)
  4. **Line Chart**: "Monthly Attrition Over Time"
     * X-Axis: `Dim_Date[Year Month]`
     * Y-Axis: `[Employees Left]` (Note: Change the active relationship using the measure: `Exits Over Time = CALCULATE([Employees Left], USERELATIONSHIP(Fact_Employees[Exit_Date], Dim_Date[Date]))`)
  5. **Scatter Plot**: "Exited Employees Tenure vs. Satisfaction"
     * *First, create a calculated column in `Fact_Employees`*:
       ```dax
       Tenure Years = IF(ISBLANK(Fact_Employees[Exit_Date]), BLANK(), DIVIDE(DATEDIFF(Fact_Employees[Joining_Date], Fact_Employees[Exit_Date], DAY), 365, 2))
       ```
     * Details: `Fact_Employees[Employee_ID]`
     * X-Axis: `Fact_Employees[Tenure Years]`
     * Y-Axis: `Fact_Employees[Satisfaction_Score]`

---

### PAGE 4: PERFORMANCE & SATISFACTION
* **KPI Cards**:
  * `[Average Performance]`, `[Average Satisfaction]`, `[Average Training Hours]`
* **Visuals**:
  1. **Scatter Plot**: "Employee Performance vs. Satisfaction Grid"
     * Details: `Fact_Employees[Employee_ID]`
     * X-Axis: `Fact_Employees[Satisfaction_Score]` (Right-click and set to **Don't Summarize** or pull `[Average Satisfaction]`)
     * Y-Axis: `Fact_Employees[Performance_Score]` (or `[Average Performance]`)
     * *Add a reference line on the chart canvas (Analytics Pane > Constant Line) at X=3.0 and Y=3.0 to isolate the 4 quadrants.*
  2. **Clustered Column Chart**: "Performance & Satisfaction by Department"
     * X-Axis: `Fact_Employees[Department]`
     * Y-Axis: `[Average Performance]` and `[Average Satisfaction]` (side-by-side)
  3. **Line & Stacked Column Chart**: "Upskilling ROI (Training Hours vs. Performance)"
     * *Create a Group for training hours*: Right-click `Fact_Employees[Training_Hours]` > **New Group** > Bin size 20.
     * X-Axis: `Fact_Employees[Training_Hours (bins)]`
     * Column Values: `[Total Employees]`
     * Line Values: `[Average Performance]`
  4. **Scatter Chart**: "Absenteeism Impact on Work Performance"
     * X-Axis: `Fact_Employees[Absenteeism_Days]`
     * Y-Axis: `[Average Performance]`
     * Legend: `Fact_Employees[Department]`

---

### PAGE 5: WORKFORCE DEMOGRAPHICS & COMPENSATION
* **Visuals**:
  1. **Clustered Column Chart**: "Salary Equity: Department & Gender"
     * X-Axis: `Fact_Employees[Department]`
     * Legend: `Fact_Employees[Gender]`
     * Y-Axis: `[Average Salary]`
  2. **Treemap**: "Employee Distribution by Location"
     * Group: `Fact_Employees[Location]`
     * Values: `[Total Employees]`
  3. **Donut Chart**: "Workforce Education Levels"
     * Legend: `Fact_Employees[Education]`
     * Values: `[Total Employees]`
  4. **Scatter Plot**: "Experience vs. Salary Curve"
     * Details: `Fact_Employees[Employee_ID]`
     * X-Axis: `Fact_Employees[Experience_Years]`
     * Y-Axis: `Fact_Employees[Salary]`
     * Legend: `Fact_Employees[Department]`

---

## 7. Drill-Through Setup
To allow users to select a department and inspect specific employee profiles:
1. Create a new page and name it **"Department Details"**.
2. In the Visualizations pane, scroll down to the **Drill-through** section. Drag `Fact_Employees[Department]` into the **"Add drill-through fields here"** box.
3. Power BI will automatically create a **Back Button** on the top-left of the canvas.
4. Add a **Table Visual** to the canvas and drag in the following columns:
   * `Employee_ID`, `Employee_Name`, `Job_Role`, `Location`, `Experience_Years`, `Salary`, `Performance_Score`, `Satisfaction_Score`, `Overtime_Hours`.
5. Now, a user can go to Page 1, right-click on any department bar, select **Drillthrough** > **Department Details**, and view the filtered list of employees.

---

## 8. Sourcing & Setup of Hiring Forecast (Page 6)
You can set up two types of hiring forecasts on Page 6:

### Option A: Using the Python ML Regression Outputs (Recommended)
1. Add a **Line Chart** to the canvas.
2. Drag `Fact_HiringForecast[Date]` to the **X-Axis**.
3. Drag `Fact_HiringForecast[Historical_Hires]` and `Fact_HiringForecast[Forecasted_Hires]` to the **Y-Axis**.
4. In the Formatting pane, set:
   * `Historical_Hires` line color to dark navy blue (`#1D3557`) with a solid line style.
   * `Forecasted_Hires` line color to green (`#2A9D8F`) with a **dashed** line style.

### Option B: Power BI Native Forecasting Tool
1. Add a standard **Line Chart** to the canvas.
2. Drag `Dim_Date[Date]` (aggregated by year-month) to the **X-Axis**.
3. Drag `[Total Joined]` (or employee headcount) to the **Y-Axis**.
4. With the visual selected, click the **Analytics** tab (magnifying glass icon under the Visualizations pane).
5. Scroll down and expand the **Forecast** tab > click **+ Add**.
6. Set:
   * Forecast Length = **6 Months**
   * Confidence Interval = **95%**
   * Seasonality = **12** (helps capture yearly seasonal loops)
7. Click **Apply**. A shaded blue forecast zone will appear at the end of the timeline.

---

## 9. Key Actionable Insights (Derived from Data)

1. **Burnout Alert in Sales & Customer Service**: 
   * **Observation**: Sales and CS exhibit attrition rates exceeding 20% (the company average is 12%). This is highly correlated with average overtime hours exceeding 120 hours annually and low satisfaction scores (1 or 2).
   * **Action**: Cap overtime hours in these departments at 80 hours per year and review compensation structures.
2. **Upskilling ROI**:
   * **Observation**: Employees with >60 hours of training score an average of 4.1 in performance, compared to 2.8 for employees with <20 hours.
   * **Action**: Create a mandatory upskilling threshold of 40 hours per year for all mid-level roles.
3. **Optimizing Sourcing Channels**:
   * **Observation**: Referrals average \$650 in recruitment cost and show the lowest attrition rate (~5%). Executive Search costs \$18,000 per hire.
   * **Action**: Reallocate 20% of the Executive Search budget to launch a referral bonus program.

---

## START HERE: Your First 5 Actions in Power BI Desktop

Follow these 5 steps to start building the report:

1. **Step 1: Import the Data**
   Open Power BI Desktop. Click **Get Data** > **Text/CSV**. Navigate to your workspace directory `c:\Users\Newman\Documents\HR_Analytics_Project\data\` and open `employees.csv`. Click **Transform Data** (not Load).
2. **Step 2: Add and Rename the Queries**
   Inside Power Query, add the other three CSV files (`recruitment.csv`, `performance.csv`, `hiring_forecast_output.csv`). Right-click each query name on the left panel and rename them to: `Fact_Employees`, `Fact_Recruitment`, `Fact_Performance`, and `Fact_HiringForecast`.
3. **Step 3: Correct Column Data Types**
   Scan the tables and ensure all date columns are set to the **Date** data type, IDs are set to **Text**, values like `Salary` are set to **Fixed Decimal Number** (Currency), and scores/hours are set to **Whole Number**. Click **Close & Apply** to load the tables.
4. **Step 4: Create the Dim_Date Table**
   In the main screen, go to the Modeling tab and click **New Table**. Paste the `Dim_Date` DAX calendar code (from Section 3 of this guide). Mark this table as a Date table.
5. **Step 5: Link Your Tables in the Model View**
   Navigate to the **Model View** (the third icon on the left sidebar). Drag fields to create relationships between tables, ensuring that the primary date links (like `Joining_Date`, `Review_Date`, and `Application_Date`) are active.
