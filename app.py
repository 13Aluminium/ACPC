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
    
    # Remove newlines
    course_name = course_name.replace('\n', ' ')
    
    # Remove the " - TFWS" or " - TFW" suffix
    course_name = re.sub(r'\s*-\s*(TFWS|TFW)$', '', course_name)
    
    return course_name.strip()

# Load filter options from the JSON file
with open('0.json', 'r') as f:
    filter_options = json.load(f)

# Process the course names to create a normalized list
normalized_courses = set()
course_mapping = {}  # Maps normalized names to original names

for course in filter_options["Course_name"]:
    normalized = normalize_course_name(course)
    normalized_courses.add(normalized)
    
    # Create a mapping from normalized name to original name
    if normalized not in course_mapping:
        course_mapping[normalized] = []
    course_mapping[normalized].append(course)

# Replace the course list with the normalized unique list
filter_options["Course_name"] = sorted(list(normalized_courses))

# Function to load CSV data based on round
def load_csv_data(round_num):
    df = None
    
    if round_num == 1:
        # Load mock round data
        if os.path.exists('0.csv'):
            df = pd.read_csv('0.csv')
        else:
            df = pd.DataFrame(columns=['Inst_Name', 'Course_name', 'Alloted_Cat', 'Quota', 'Institute Type', 'First Rank', 'Last Rank', 'City'])
    elif round_num == 2:
        # Load first round data
        if os.path.exists('1-1.csv'):
            df = pd.read_csv('1-1.csv')
        else:
            df = pd.DataFrame(columns=['Inst_Name', 'Course_name', 'Alloted_Cat', 'Quota', 'Institute Type', 'First Rank', 'Last Rank', 'City'])
    elif round_num == 3:
        # Load third round data
        if os.path.exists('2-1.csv'):
            df = pd.read_csv('2-1.csv')
        else:
            df = pd.DataFrame(columns=['Inst_Name', 'Course_name', 'Alloted_Cat', 'Quota', 'Institute Type', 'First Rank', 'Last Rank', 'City'])
    
    if df is not None and not df.empty and 'Course_name' in df.columns:
        # Add normalized course names to the dataframe
        df['Normalized_Course'] = df['Course_name'].apply(normalize_course_name)
    
    return df

@app.route('/')
def index():
    return render_template('index.html', filter_options=filter_options)

@app.route('/filter_data', methods=['POST'])
def filter_data():
    # Get filter criteria from request
    filters = request.get_json()
    round_num = int(filters.get('Round', 1))
    
    # Load data for the selected round
    df = load_csv_data(round_num)
    
    if df is None or df.empty:
        return jsonify({'data': [], 'message': 'No data available for this round'})
    
    # Apply filters
    filtered_df = df.copy()
    
    if filters.get('Course_name'):
        # Use the normalized course name for filtering
        normalized_filter = normalize_course_name(filters['Course_name'])
        filtered_df = filtered_df[filtered_df['Normalized_Course'] == normalized_filter]
    
    if filters.get('Alloted_Cat'):
        filtered_df = filtered_df[filtered_df['Alloted_Cat'] == filters['Alloted_Cat']]
    
    if filters.get('Quota'):
        filtered_df = filtered_df[filtered_df['Quota'] == filters['Quota']]
    
    if filters.get('Institute Type'):
        filtered_df = filtered_df[filtered_df['Institute Type'] == filters['Institute Type']]
    
    if filters.get('City'):
        filtered_df = filtered_df[filtered_df['City'] == filters['City']]
    
    # Sort by First Rank
    if not filtered_df.empty:
        try:
            filtered_df = filtered_df.sort_values('First Rank')
        except:
            pass  # In case First Rank is not a numeric column
    
    # Remove normalized course column from output
    if 'Normalized_Course' in filtered_df.columns:
        filtered_df = filtered_df.drop('Normalized_Course', axis=1)
    
    result = filtered_df.to_dict('records')
    return jsonify({'data': result})
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
