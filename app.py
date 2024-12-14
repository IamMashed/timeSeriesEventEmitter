from flask import Flask, jsonify, Response, request
from flask_sqlalchemy import SQLAlchemy
import time
import threading
import json
from datetime import datetime
import random

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<username>:<password>@db:5432/time_series_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Database model for events
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    metric = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)


# Store the current interval (default: 5 seconds)
current_interval = 5


@app.route('/stream')
def stream():
    """
    Event Stream endpoint that emits time-series data continuously.
    """
    def generate_events():
        with app.app_context():  # Make sure to push the application context here
            while True:
                # Create a random metric as an example
                event = {
                    'timestamp': datetime.utcnow().isoformat() + 'Z',
                    'metric': 'temperature',  # Example metric
                    'value': round(random.uniform(20.0, 30.0), 2)
                }
                # Emit event to the client
                yield f"data: {json.dumps(event)}\n\n"
                # Store the event in the database
                new_event = Event(
                    timestamp=datetime.utcnow(),
                    metric=event['metric'],
                    value=event['value']
                )
                db.session.add(new_event)
                db.session.commit()
                # Wait for the specified interval
                time.sleep(current_interval)

    return Response(generate_events(), content_type='text/event-stream')


@app.route('/history')
def history():
    """
    Retrieve the last N events from the database.
    """
    n = request.args.get('n', default=10, type=int)  # Default to 10 events
    events = Event.query.order_by(Event.id.desc()).limit(n).all()
    # TODO: Rework db query to avoid converting event objects to dictionaries
    events_list = [{
        "timestamp": event.timestamp.isoformat() + 'Z',
        "metric": event.metric,
        "value": event.value
    } for event in events]
    return jsonify(events_list)


@app.route('/set_interval', methods=['POST'])
def set_interval():
    global current_interval
    data = request.get_json()
    if data and "interval" in data:
        current_interval = data["interval"]
        return jsonify({"message": f"Interval set to {current_interval} seconds"}), 200
    else:
        return jsonify({"error": "Invalid payload"}), 400


if __name__ == '__main__':
    # Flask app
    app.run(host='0.0.0.0', port=5000)
