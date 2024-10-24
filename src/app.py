from flask import Flask, jsonify
from weather_monitor import weather_data, alerts

app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def get_weather_data():
    """Endpoint to get the current weather data."""
    return jsonify(weather_data)

@app.route('/alerts', methods=['GET'])
def get_alerts():
    """Endpoint to get the current alerts."""
    return jsonify(alerts)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
