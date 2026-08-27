# Hiring Forecast Model Documentation

This document describes the predictive analytics model built to forecast future hiring requirements for the HR Analytics Dashboard.

## Model Summary
- **Selected Algorithm**: Linear Regression (Trend Analysis)
- **Why Selected**: Simple, highly explainable, and ideal for a junior/fresher project. It fits a straight line through historical data points to capture long-term company growth.
- **Input Feature**: `Month_Index` (Time index representing consecutive months from January 2020 onwards).
- **Target Variable**: `Hires` (Total headcount hired in that month).
- **Forecast Horizon**: 6 Months (July 2026 to December 2026).

## Equations and Parameters
- **Formula**: `Monthly_Hires = -0.0318 * Month_Index + 29.46`
- **Interpretation**: The slope of `-0.0318` indicates that the organization's hiring volume is changing by approximately `-0.03` hires per month.

## Performance Metrics
- **Mean Absolute Error (MAE)**: 4.60 hires/month (On average, the model's historical predictions deviate by 4.60 hires from actual data).
- **Root Mean Squared Error (RMSE)**: 5.79 hires/month (Penalizes larger errors more heavily).

## 6-Month Hiring Forecast Results
- **July 2026**: 27 forecasted hires
- **August 2026**: 27 forecasted hires
- **September 2026**: 27 forecasted hires
- **October 2026**: 27 forecasted hires
- **November 2026**: 27 forecasted hires
- **December 2026**: 27 forecasted hires

## Model Assumptions
1. **Linear Trend**: Assumes hiring growth continues at a constant, linear pace based on historical patterns.
2. **No Macroeconomic Shocks**: Assumes no major external economic shocks, mergers, or changes in hiring budget.
3. **No Strong Short-Term Seasonality**: Assumes long-term growth is a stronger driver than individual seasonal months (though minor seasonality is handled visually in Power BI).

## Limitations
- **Lacks Seasonality Adjustment**: A simple linear trend doesn't capture annual hiring freezes (e.g., December) or peak hiring seasons (e.g., graduation months in June/July).
- **No External Features**: The model only relies on time as a feature and doesn't incorporate business revenue, attrition trends, or department-level budgets.
- **Not Guaranteed**: All predictive models are estimations and should be used as a guide rather than a guarantee.
