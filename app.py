from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import os
import re

app = Flask(__name__)

# Normalize course names by removing line breaks and standardizing names
def normalize_course_name(course_name):
    if not isinstance(course_name, str):
        return ""
    course_name = course_name.replace('\n', ' ')
    course_name = re.sub(r'\s*-\s*(TFWS|TFW)$', '', course_name)
    return course_name.strip()

# Function to lazily load and normalize filter options
def get_filter_options():
    try:
        with open('0.json', 'r') as f:
            filter_options = json.load(f)
    except FileNotFoundError:
        return {"Course_name": []}

    normalized_courses = set()
    course_mapping = {}

    for course in filter_options.get("Course_name", []):
        normalized = normalize_course_name(course)
        normalized_courses.add(normalized)
        course_mapping.setdefault(normalized, []).append(course)

    filter_options["Course_name"] = sorted(list(normalized_courses))
    return filter_options

# Function to load CSV data based on round
def load_csv_data(round_num):
    filename = {
        1: '0.csv',
        2: '1-1.csv',
        3: '2-1.csv'
    }.get(round_num)

    if filename and os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=[
            'Inst_Name', 'Course_name', 'Alloted_Cat', 'Quota',
            'Institute Type', 'First Rank', 'Last Rank', 'City'
        ])
    
    if not df.empty and 'Course_name' in df.columns:
        df['Normalized_Course'] = df['Course_name'].apply(normalize_course_name)

    return df

@app.route('/')
def index():
    filter_options = get_filter_options()
    return render_template('index.html', filter_options=filter_options)

@app.route('/filter_data', methods=['POST'])
def filter_data():
    filters = request.get_json()
    round_num = int(filters.get('Round', 1))
    df = load_csv_data(round_num)

    if df.empty:
        return jsonify({'data': [], 'message': 'No data available for this round'})

    filtered_df = df.copy()

    if filters.get('Course_name'):
        normalized_filter = normalize_course_name(filters['Course_name'])
        filtered_df = filtered_df[filtered_df['Normalized_Course'] == normalized_filter]

    for key in ['Alloted_Cat', 'Quota', 'Institute Type', 'City']:
        if filters.get(key):
            filtered_df = filtered_df[filtered_df[key] == filters[key]]

    if not filtered_df.empty:
        try:
            filtered_df = filtered_df.sort_values('First Rank')
        except:
            pass

    if 'Normalized_Course' in filtered_df.columns:
        filtered_df.drop('Normalized_Course', axis=1, inplace=True)

    result = filtered_df.to_dict('records')
    return jsonify({'data': result})

if __name__ == '__main__':
    app.run(debug=True)
