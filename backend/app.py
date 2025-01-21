from flask import Flask, jsonify
from ics import Calendar
from datetime import timedelta
import json

app = Flask(__name__)

# Function to load and parse ICS file
def load_ics_file(file_path):
    with open(file_path, 'r') as f:
        calendar = Calendar(f.read())
    return list(calendar.events)

# Function to find available slots
def find_available_slots(events, min_gap_minutes=30, start_hour=8, end_hour=18):
    available_slots = []
    daytime_start = timedelta(hours=start_hour)
    daytime_end = timedelta(hours=end_hour)
    for i in range(len(events) - 1):
        current_event_end = events[i].end
        next_event_start = events[i + 1].begin
        gap = next_event_start - current_event_end
        if gap >= timedelta(minutes=min_gap_minutes):
            current_event_end_time = timedelta(hours=current_event_end.hour, minutes=current_event_end.minute)
            next_event_start_time = timedelta(hours=next_event_start.hour, minutes=next_event_start.minute)
            if current_event_end_time >= daytime_start and next_event_start_time <= daytime_end:
                available_slots.append({
                    "start": current_event_end.isoformat(),  # Convert Arrow object to string
                    "end": next_event_start.isoformat()     # Convert Arrow object to string
                })
    return available_slots

# Convert event to dictionary for API response
def event_to_dict(event):
    return {
        "name": event.name,
        "begin": event.begin.isoformat(),  # Convert Arrow object to string
        "end": event.end.isoformat(),      # Convert Arrow object to string
        "location": event.location,
        "description": event.description
    }

@app.route('/events')
def get_events():
    events = load_ics_file('tasks.ics')  # Replace with the actual path of your ICS file
    return jsonify([event_to_dict(event) for event in events])

@app.route('/available_slots')
def get_available_slots():
    events = load_ics_file('tasks.ics')
    slots = find_available_slots(events)
    return jsonify(slots)

if __name__ == '__main__':
    app.run(debug=True)
