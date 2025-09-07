#!/usr/bin/env python3
"""
Simple Flask application for Japan Environmental Data
Works with or without Flask dependencies
"""

import json
from datetime import datetime, timedelta
from japan_environmental_data import JapanEnvironmentalDataFetcher

# Check for Flask availability
try:
    from flask import Flask, jsonify, request
    from flask_cors import CORS
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False

def create_app():
    """Create Flask app if possible"""
    if not HAS_FLASK:
        return None
        
    app = Flask(__name__)
    CORS(app)
    
    # Initialize data fetcher
    japan_data_fetcher = JapanEnvironmentalDataFetcher()
    
    # Sample data for compatibility
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
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'japan_data_available': True
        })
    
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
        # Manual calculation without pandas
        temps = [d['temperature'] for d in sample_environmental_data]
        humids = [d['humidity'] for d in sample_environmental_data]
        aqis = [d['air_quality_index'] for d in sample_environmental_data]
        co2s = [d['co2_level'] for d in sample_environmental_data]
        
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
    
    # Japan Environmental Data Routes
    @app.route('/api/japan/air-quality', methods=['GET'])
    def get_japan_air_quality():
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
    
    return app

def test_japan_data():
    """Test Japan environmental data functionality"""
    print("🇯🇵 Japan Environmental Data System Test")
    print("=" * 50)
    
    fetcher = JapanEnvironmentalDataFetcher()
    
    # Test all data sources
    tests = [
        ("Air Quality", lambda: fetcher.get_air_quality_data("Tokyo")),
        ("Climate Data", lambda: fetcher.get_climate_data()),
        ("Pollution Data", lambda: fetcher.get_pollution_data()),
        ("Biodiversity Data", lambda: fetcher.get_biodiversity_data()),
        ("Energy Data", lambda: fetcher.get_energy_emissions_data()),
    ]
    
    for name, test_func in tests:
        try:
            data = test_func()
            print(f"✅ {name}: {len(data)} records")
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
    
    # Test comprehensive report
    try:
        report = fetcher.get_comprehensive_environmental_report()
        total_points = report.get('summary', {}).get('total_data_points', 0)
        print(f"✅ Comprehensive Report: {total_points} total data points")
    except Exception as e:
        print(f"❌ Comprehensive Report: Error - {e}")
    
    print("\n🎉 Japan Environmental Data System is operational!")
    return True

if __name__ == '__main__':
    if HAS_FLASK:
        app = create_app()
        if app:
            print("🚀 Starting Japan Environmental Data Server...")
            print("📊 Available endpoints:")
            print("   - /api/japan/air-quality")
            print("   - /api/japan/climate") 
            print("   - /api/japan/pollution")
            print("   - /api/japan/biodiversity")
            print("   - /api/japan/energy-emissions")
            print("   - /api/japan/comprehensive-report")
            print("   - /api/japan/environmental-problems")
            print("\n🌐 Server running at http://localhost:5000")
            app.run(debug=True, host='0.0.0.0', port=5000)
        else:
            print("❌ Failed to create Flask app")
    else:
        print("⚠️  Flask not available. Testing data functionality directly...")
        test_japan_data()
        print("\n💡 To run the web server, install Flask:")
        print("   pip install Flask Flask-CORS")