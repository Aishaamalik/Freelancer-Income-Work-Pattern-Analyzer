import pandas as pd
import numpy as np

def load_and_clean_data(csv_path):
    """
    Loads and cleans the freelancer earnings CSV data.
    Args:
        csv_path (str): Path to the CSV file.
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = pd.read_csv(csv_path)

    # Remove duplicates
    df = df.drop_duplicates()

    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    # Handle missing values
    # Drop rows where critical columns are missing
    critical_cols = ['Freelancer_ID', 'Earnings_USD']
    df = df.dropna(subset=critical_cols)

    # Fill missing numeric columns with median
    for col in numeric_cols:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].median())

    # Fill missing categorical columns with mode
    for col in categorical_cols:
        if df[col].isnull().any():
            mode = df[col].mode()
            if not mode.empty:
                df[col] = df[col].fillna(mode[0])
            else:
                df[col] = df[col].fillna('Unknown')

    # Ensure correct data types
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    for col in categorical_cols:
        df[col] = df[col].astype(str)

    # Remove outliers (outside 1st and 99th percentiles) for numeric columns
    for col in numeric_cols:
        lower = df[col].quantile(0.01)
        upper = df[col].quantile(0.99)
        df = df[(df[col] >= lower) & (df[col] <= upper)]

    df = df.reset_index(drop=True)
    return df 

def analyze_earnings(df):
    """
    Returns total and average earnings.
    """
    total_earnings = float(df['Earnings_USD'].sum())
    avg_earnings = float(df['Earnings_USD'].mean())
    return {'total_earnings': total_earnings, 'average_earnings': avg_earnings}


def hourly_rate_distribution(df):
    """
    Returns basic statistics and histogram data for hourly rates.
    """
    desc = df['Hourly_Rate'].describe().to_dict()
    hist = np.histogram(df['Hourly_Rate'], bins=10)
    return {'description': desc, 'histogram': {'bins': hist[1].tolist(), 'counts': hist[0].tolist()}}


def skill_earnings(df):
    """
    Returns total and average earnings by job category (skill).
    """
    skill_group = df.groupby('Job_Category')['Earnings_USD'].agg(['sum', 'mean']).reset_index()
    return skill_group.to_dict(orient='records')


def job_success_scores(df):
    """
    Returns average job success rate and client rating by platform.
    """
    platform_group = df.groupby('Platform').agg({'Job_Success_Rate': 'mean', 'Client_Rating': 'mean'}).reset_index()
    return platform_group.to_dict(orient='records')


def simulate_time_series(df, periods=24):
    """
    Simulates monthly earnings data for time-based analysis if date is not available.
    Returns a DataFrame with synthetic 'Month' and 'Earnings_USD'.
    """
    np.random.seed(42)
    months = [f'Month_{i+1}' for i in range(periods)]
    # Simulate total earnings per month based on overall distribution
    earnings = np.random.normal(df['Earnings_USD'].mean(), df['Earnings_USD'].std(), periods)
    earnings = np.clip(earnings, 0, None)
    return pd.DataFrame({'Month': months, 'Earnings_USD': earnings})


def forecast_earnings(df, periods=6):
    """
    Forecasts future earnings using a simple ML model (linear regression) on simulated time series.
    Returns forecasted earnings for the next 'periods' months.
    """
    from sklearn.linear_model import LinearRegression
    # Simulate time series
    ts_df = simulate_time_series(df)
    ts_df['Month_Num'] = np.arange(len(ts_df))
    X = ts_df[['Month_Num']]
    y = ts_df['Earnings_USD']
    model = LinearRegression()
    model.fit(X, y)
    future_months = np.arange(len(ts_df), len(ts_df) + periods).reshape(-1, 1)
    forecast = model.predict(future_months)
    return {'future_months': [f'Month_{i+1}' for i in range(len(ts_df), len(ts_df) + periods)], 'forecasted_earnings': [float(x) for x in forecast]} 