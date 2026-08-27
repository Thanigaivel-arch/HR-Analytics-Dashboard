import os
import pandas as pd
import numpy as np
from datetime import datetime

# Fallbacks in case libraries aren't installed, though they should be
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

def generate_forecast():
    print("Starting predictive analysis and hiring forecast...")
    
    # 1. Load data
    if not os.path.exists('data/employees.csv'):
        print("Error: data/employees.csv not found. Run data_generation.py first.")
        return
        
    df = pd.read_csv('data/employees.csv')
    df['Joining_Date'] = pd.to_datetime(df['Joining_Date'])
    
    # 2. Aggregate monthly hiring counts
    # We will count how many employees joined each year-month
    df['Year_Month'] = df['Joining_Date'].dt.to_period('M')
    monthly_hires = df.groupby('Year_Month').size().reset_index(name='Hires')
    
    # Standardize to datetime for easier plotting/handling
    monthly_hires['Date'] = monthly_hires['Year_Month'].dt.to_timestamp()
    monthly_hires = monthly_hires.sort_values('Date').reset_index(drop=True)
    
    # We filter out the last month if it is incomplete (e.g. August 2026, since our generation went to June 30, 2026)
    # Our data generation ends on June 30, 2026, so everything up to June 2026 is complete.
    monthly_hires = monthly_hires[monthly_hires['Date'] <= '2026-06-30'].copy()
    
    # Add a time index column (1, 2, 3...) representing consecutive months
    monthly_hires['Month_Index'] = np.arange(len(monthly_hires)) + 1
    
    # 3. Model Training
    X = monthly_hires[['Month_Index']].values
    y = monthly_hires['Hires'].values
    
    forecast_months = 6
    future_indices = np.arange(len(monthly_hires) + 1, len(monthly_hires) + 1 + forecast_months).reshape(-1, 1)
    
    if SKLEARN_AVAILABLE:
        # Fit Linear Regression
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict historical values to calculate error
        y_pred = model.predict(X)
        
        # Calculate error metrics
        mae = mean_absolute_error(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        
        # Predict future hires
        future_preds = model.predict(future_indices)
        
        # Extract coefficient (slope) and intercept
        slope = model.coef_[0]
        intercept = model.intercept_
    else:
        # Fallback to numpy polyfit
        slope, intercept = np.polyfit(monthly_hires['Month_Index'], monthly_hires['Hires'], 1)
        y_pred = slope * monthly_hires['Month_Index'] + intercept
        
        # Calculate MAE and RMSE
        mae = np.mean(np.abs(y - y_pred))
        rmse = np.sqrt(np.mean((y - y_pred)**2))
        
        future_preds = slope * future_indices.flatten() + intercept
        
    print(f"Model Evaluation Summary:")
    print(f"- Algorithm: Linear Regression (Trend-based)")
    print(f"- Mean Absolute Error (MAE): {mae:.2f} hires/month")
    print(f"- Root Mean Squared Error (RMSE): {rmse:.2f} hires/month")
    print(f"- Regression Formula: Hires = {slope:.3f} * Month_Index + {intercept:.2f}")
    
    # 4. Prepare Forecast Output Dataset
    # We will generate future dates
    last_date = monthly_hires['Date'].max()
    future_dates = [last_date + pd.DateOffset(months=m) for m in range(1, forecast_months + 1)]
    
    # Construct historical DataFrame for output
    historical_out = pd.DataFrame({
        'Date': monthly_hires['Date'].dt.strftime('%Y-%m-%d'),
        'Historical_Hires': monthly_hires['Hires'],
        'Forecasted_Hires': np.nan,
        'Type': 'Actual'
    })
    
    # Construct future DataFrame for output (rounding forecast to nearest integer)
    future_preds_rounded = np.clip(np.round(future_preds), 0, None)
    future_out = pd.DataFrame({
        'Date': [d.strftime('%Y-%m-%d') for d in future_dates],
        'Historical_Hires': np.nan,
        'Forecasted_Hires': future_preds_rounded,
        'Type': 'Forecast'
    })
    
    # Combine actuals and forecast
    combined_df = pd.concat([historical_out, future_out], ignore_index=True)
    combined_df.to_csv('data/hiring_forecast_output.csv', index=False)
    print(f"Forecast output saved to 'data/hiring_forecast_output.csv'.")
    
    # 5. Generate Plot Visualization
    if MATPLOTLIB_AVAILABLE:
        os.makedirs('screenshots', exist_ok=True)
        plt.figure(figsize=(10, 5))
        plt.plot(monthly_hires['Date'], monthly_hires['Hires'], marker='o', label='Actual Hires', color='#2b5c8f', linewidth=2)
        
        # Plot regression trend-line
        plt.plot(monthly_hires['Date'], y_pred, linestyle='--', color='#d9534f', label='Historical Trend-line')
        
        # Plot future forecast
        plt.plot(future_dates, future_preds_rounded, marker='s', color='#2ca02c', label='6-Month Forecast', linewidth=2)
        
        # Add labels and formatting
        plt.title('Monthly Employee Hiring Trend & 6-Month Forecast', fontsize=14, fontweight='bold', pad=15)
        plt.xlabel('Date', fontsize=11, labelpad=10)
        plt.ylabel('Hires Count', fontsize=11, labelpad=10)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.legend(loc='upper left', frameon=True)
        plt.tight_layout()
        
        plt.savefig('screenshots/hiring_forecast.png', dpi=150)
        print("Visualization plot saved to 'screenshots/hiring_forecast.png'.")
        plt.close()
        
    # Write model metadata to a text file for Power BI reference / student prep
    with open('documentation/Forecasting_Model_Details.md', 'w') as f:
        f.write(f"""# Hiring Forecast Model Documentation

This document describes the predictive analytics model built to forecast future hiring requirements for the HR Analytics Dashboard.

## Model Summary
- **Selected Algorithm**: Linear Regression (Trend Analysis)
- **Why Selected**: Simple, highly explainable, and ideal for a junior/fresher project. It fits a straight line through historical data points to capture long-term company growth.
- **Input Feature**: `Month_Index` (Time index representing consecutive months from January 2020 onwards).
- **Target Variable**: `Hires` (Total headcount hired in that month).
- **Forecast Horizon**: 6 Months (July 2026 to December 2026).

## Equations and Parameters
- **Formula**: `Monthly_Hires = {slope:.4f} * Month_Index + {intercept:.2f}`
- **Interpretation**: The slope of `{slope:.4f}` indicates that the organization's hiring volume is changing by approximately `{slope:.2f}` hires per month.

## Performance Metrics
- **Mean Absolute Error (MAE)**: {mae:.2f} hires/month (On average, the model's historical predictions deviate by {mae:.2f} hires from actual data).
- **Root Mean Squared Error (RMSE)**: {rmse:.2f} hires/month (Penalizes larger errors more heavily).

## 6-Month Hiring Forecast Results
""")
        for d, pred in zip(future_dates, future_preds_rounded):
            f.write(f"- **{d.strftime('%B %Y')}**: {int(pred)} forecasted hires\n")
            
        f.write("""
## Model Assumptions
1. **Linear Trend**: Assumes hiring growth continues at a constant, linear pace based on historical patterns.
2. **No Macroeconomic Shocks**: Assumes no major external economic shocks, mergers, or changes in hiring budget.
3. **No Strong Short-Term Seasonality**: Assumes long-term growth is a stronger driver than individual seasonal months (though minor seasonality is handled visually in Power BI).

## Limitations
- **Lacks Seasonality Adjustment**: A simple linear trend doesn't capture annual hiring freezes (e.g., December) or peak hiring seasons (e.g., graduation months in June/July).
- **No External Features**: The model only relies on time as a feature and doesn't incorporate business revenue, attrition trends, or department-level budgets.
- **Not Guaranteed**: All predictive models are estimations and should be used as a guide rather than a guarantee.
""")
    print("Forecasting documentation saved to 'documentation/Forecasting_Model_Details.md'.")

if __name__ == '__main__':
    generate_forecast()
