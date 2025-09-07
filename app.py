try:
    from flask import Flask, jsonify, request
    from flask_cors import CORS
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("Flask not available. Please install Flask to run the web server.")

import json
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False

from datetime import datetime, timedelta
from japan_environmental_data import JapanEnvironmentalDataFetcher

if HAS_FLASK:
    app = Flask(__name__)
    CORS(app)
else:
    app = None

# 日本環境データフェッチャーのインスタンス
japan_data_fetcher = JapanEnvironmentalDataFetcher()

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

# Only define routes if Flask is available
if HAS_FLASK and app:
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
    if HAS_PANDAS:
        df = pd.DataFrame(sample_environmental_data)
    else:
        # Manual calculation without pandas
        df = sample_environmental_data
    
    if HAS_PANDAS:
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
    else:
        # Manual calculation without pandas
        temps = [d['temperature'] for d in df]
        humids = [d['humidity'] for d in df]
        aqis = [d['air_quality_index'] for d in df]
        co2s = [d['co2_level'] for d in df]
        
        stats = {
            'temperature': {
                'avg': sum(temps) / len(temps),
                'min': min(temps),
                'max': max(temps)
            },
            'humidity': {
                'avg': sum(humids) / len(humids),
                'min': min(humids),
                'max': max(humids)
            },
            'air_quality_index': {
                'avg': sum(aqis) / len(aqis),
                'min': min(aqis),
                'max': max(aqis)
            },
            'co2_level': {
                'avg': sum(co2s) / len(co2s),
                'min': min(co2s),
                'max': max(co2s)
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

# 日本の環境問題データ用の新しいエンドポイント

@app.route('/api/japan/air-quality', methods=['GET'])
def get_japan_air_quality():
    """日本の大気質データを取得"""
    try:
        prefecture = request.args.get('prefecture', 'Tokyo')
        data = japan_data_fetcher.get_air_quality_data(prefecture)
        
        return jsonify({
            'status': 'success',
            'data': data,
            'count': len(data),
            'prefecture': prefecture
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/japan/climate', methods=['GET'])
def get_japan_climate_data():
    """日本の気候変動データを取得"""
    try:
        data = japan_data_fetcher.get_climate_data()
        
        return jsonify({
            'status': 'success',
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/japan/pollution', methods=['GET'])
def get_japan_pollution_data():
    """日本の汚染データを取得"""
    try:
        data = japan_data_fetcher.get_pollution_data()
        
        return jsonify({
            'status': 'success',
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/japan/biodiversity', methods=['GET'])
def get_japan_biodiversity_data():
    """日本の生物多様性データを取得"""
    try:
        data = japan_data_fetcher.get_biodiversity_data()
        
        return jsonify({
            'status': 'success',
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/japan/energy-emissions', methods=['GET'])
def get_japan_energy_emissions():
    """日本のエネルギーとCO2排出データを取得"""
    try:
        data = japan_data_fetcher.get_energy_emissions_data()
        
        return jsonify({
            'status': 'success',
            'data': data,
            'count': len(data)
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/japan/comprehensive-report', methods=['GET'])
def get_japan_comprehensive_report():
    """日本の包括的環境レポートを取得"""
    try:
        report = japan_data_fetcher.get_comprehensive_environmental_report()
        
        return jsonify({
            'status': 'success',
            'report': report
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/japan/environmental-problems', methods=['GET'])
def get_japan_environmental_problems():
    """日本の環境問題の概要を取得"""
    try:
        problems = {
            'major_issues': [
                {
                    'issue': '大気汚染',
                    'description': '都市部でのPM2.5やNO2による大気汚染が健康に影響',
                    'severity': 'high',
                    'affected_areas': ['東京', '大阪', '名古屋'],
                    'trend': 'improving'
                },
                {
                    'issue': '気候変動',
                    'description': '地球温暖化による異常気象の増加と生態系への影響',
                    'severity': 'critical',
                    'affected_areas': ['全国'],
                    'trend': 'worsening'
                },
                {
                    'issue': '海洋汚染',
                    'description': 'プラスチック廃棄物と工業排水による海洋環境の悪化',
                    'severity': 'high',
                    'affected_areas': ['沿岸地域'],
                    'trend': 'stable'
                },
                {
                    'issue': '森林減少',
                    'description': '都市開発と林業の変化による森林面積の減少',
                    'severity': 'medium',
                    'affected_areas': ['本州', '九州'],
                    'trend': 'stable'
                },
                {
                    'issue': '生物多様性の損失',
                    'description': '絶滅危惧種の増加と生態系の破綻',
                    'severity': 'high',
                    'affected_areas': ['全国', '特に沖縄'],
                    'trend': 'worsening'
                },
                {
                    'issue': '廃棄物問題',
                    'description': '産業廃棄物と一般廃棄物の処理能力不足',
                    'severity': 'medium',
                    'affected_areas': ['都市部'],
                    'trend': 'improving'
                }
            ],
            'government_initiatives': [
                'カーボンニュートラル2050年目標',
                '再生可能エネルギーの導入促進',
                '循環型社会の構築',
                '生物多様性国家戦略',
                '大気汚染防止法の強化'
            ],
            'international_commitments': [
                'パリ協定（温室効果ガス削減）',
                '生物多様性条約',
                'SDGs（持続可能な開発目標）',
                'バーゼル条約（有害廃棄物規制）'
            ]
        }
        
        return jsonify({
            'status': 'success',
            'data': problems,
            'last_updated': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    if HAS_FLASK and app:
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Flask is not available. Please install Flask and Flask-CORS to run the web server.")
        print("You can install them with: pip install Flask Flask-CORS")
        print("\nTesting the Japan Environmental Data functionality directly...")
        
        # Test the data fetcher directly
        fetcher = JapanEnvironmentalDataFetcher()
        print("\n🇯🇵 Japan Environmental Data Test Results:")
        
        # Test air quality
        air_data = fetcher.get_air_quality_data("Tokyo")
        print(f"✅ Air Quality Data: {len(air_data)} records")
        
        # Test climate
        climate_data = fetcher.get_climate_data()
        print(f"✅ Climate Data: {len(climate_data)} records")
        
        # Test pollution
        pollution_data = fetcher.get_pollution_data()
        print(f"✅ Pollution Data: {len(pollution_data)} records")
        
        # Test biodiversity
        bio_data = fetcher.get_biodiversity_data()
        print(f"✅ Biodiversity Data: {len(bio_data)} records")
        
        # Test energy
        energy_data = fetcher.get_energy_emissions_data()
        print(f"✅ Energy Data: {len(energy_data)} records")
        
        print("\n🎉 All Japan Environmental Data functions are working!")
        print("Install Flask dependencies to access the web interface.")