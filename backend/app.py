from flask import Flask, jsonify, request
from flask_cors import CORS
from utils import (
    load_and_clean_data, analyze_earnings, hourly_rate_distribution, skill_earnings,
    job_success_scores, simulate_time_series, forecast_earnings
)
import os

app = Flask(__name__)
CORS(app)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'freelancer_earnings_bd.csv')

def get_cleaned_df():
    return load_and_clean_data(DATA_PATH)

def apply_filters(df):
    skill = request.args.get('skill')
    rate_min = request.args.get('rateMin', type=float)
    rate_max = request.args.get('rateMax', type=float)
    score = request.args.get('score', type=float)
    if skill:
        df = df[df['Job_Category'] == skill]
    if rate_min is not None:
        df = df[df['Hourly_Rate'] >= rate_min]
    if rate_max is not None:
        df = df[df['Hourly_Rate'] <= rate_max]
    if score is not None:
        df = df[df['Job_Success_Rate'] >= score]
    return df

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to the Freelancer Income & Work Pattern Analyzer API!'})

@app.route('/api/earnings-summary')
def earnings_summary():
    df = apply_filters(get_cleaned_df())
    return jsonify(analyze_earnings(df))

@app.route('/api/hourly-rate-distribution')
def hourly_rate_dist():
    df = apply_filters(get_cleaned_df())
    return jsonify(hourly_rate_distribution(df))

@app.route('/api/skill-earnings')
def skill_earnings_api():
    df = apply_filters(get_cleaned_df())
    return jsonify(skill_earnings(df))

@app.route('/api/job-success-scores')
def job_success_scores_api():
    df = apply_filters(get_cleaned_df())
    return jsonify(job_success_scores(df))

@app.route('/api/earnings-trend')
def earnings_trend():
    df = apply_filters(get_cleaned_df())
    ts_df = simulate_time_series(df)
    return jsonify(ts_df.to_dict(orient='records'))

@app.route('/api/forecast-earnings')
def forecast_earnings_api():
    df = apply_filters(get_cleaned_df())
    return jsonify(forecast_earnings(df))

@app.route('/api/skills')
def skills_api():
    df = get_cleaned_df()
    skills = sorted(df['Job_Category'].dropna().unique().tolist())
    return jsonify(skills)

if __name__ == '__main__':
    app.run(debug=True) 