from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# サンプル環境データ
sample_environmental_data = [
    {
        "id": 1,
        "date": "2024-01-01",
        "location": "Tokyo",
        "temperature": 15.2,
        "humidity": 65.3,
        "air_quality_index": 45,
        "co2_level": 420.5
    },
    {
        "id": 2,
        "date": "2024-01-02",
        "location": "Tokyo",
        "temperature": 16.8,
        "humidity": 62.1,
        "air_quality_index": 52,
        "co2_level": 425.2
    },
    {
        "id": 3,
        "date": "2024-01-03",
        "location": "Osaka",
        "temperature": 14.5,
        "humidity": 68.7,
        "air_quality_index": 38,
        "co2_level": 418.3
    }
]

@app.route('/api/environmental-data', methods=['GET'])
def get_environmental_data():
    location = request.args.get('location')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    filtered_data = sample_environmental_data.copy()
    
    if location:
        filtered_data = [data for data in filtered_data if data['location'].lower() == location.lower()]
    
    if start_date:
        filtered_data = [data for data in filtered_data if data['date'] >= start_date]
    
    if end_date:
        filtered_data = [data for data in filtered_data if data['date'] <= end_date]
    
    return jsonify({
        'status': 'success',
        'data': filtered_data,
        'count': len(filtered_data)
    })

@app.route('/api/environmental-data/statistics', methods=['GET'])
def get_statistics():
    df = pd.DataFrame(sample_environmental_data)
    
    stats = {
        'temperature': {
            'avg': float(df['temperature'].mean()),
            'min': float(df['temperature'].min()),
            'max': float(df['temperature'].max())
        },
        'humidity': {
            'avg': float(df['humidity'].mean()),
            'min': float(df['humidity'].min()),
            'max': float(df['humidity'].max())
        },
        'air_quality_index': {
            'avg': float(df['air_quality_index'].mean()),
            'min': int(df['air_quality_index'].min()),
            'max': int(df['air_quality_index'].max())
        },
        'co2_level': {
            'avg': float(df['co2_level'].mean()),
            'min': float(df['co2_level'].min()),
            'max': float(df['co2_level'].max())
        }
    }
    
    return jsonify({
        'status': 'success',
        'statistics': stats
    })

@app.route('/api/locations', methods=['GET'])
def get_locations():
    locations = list(set([data['location'] for data in sample_environmental_data]))
    return jsonify({
        'status': 'success',
        'locations': locations
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)