from ics import Calendar, Event
from datetime import datetime, timedelta

# Function to find available slots between events
def find_available_slots(events, min_gap_minutes=30, start_hour=8, end_hour=18):
    available_slots = []
    
    # Define daytime start and end time
    daytime_start = timedelta(hours=start_hour)
    daytime_end = timedelta(hours=end_hour)
    
    for i in range(len(events) - 1):
        current_event_end = events[i].end
        next_event_start = events[i + 1].begin
        
        # Check if the gap between two events is large enough
        gap = next_event_start - current_event_end
        if gap >= timedelta(minutes=min_gap_minutes):
            
            # Convert event start and end times to time deltas
            current_event_end_time = timedelta(hours=current_event_end.hour, minutes=current_event_end.minute)
            next_event_start_time = timedelta(hours=next_event_start.hour, minutes=next_event_start.minute)
            
            # Check if the available slot is within daytime hours
            if current_event_end_time >= daytime_start and next_event_start_time <= daytime_end:
                available_slots.append((current_event_end, next_event_start))
    
    return available_slots

# Function to allocate mock events into available slots
def allocate_mock_events(available_slots, event_duration_minutes=60):
    allocated_events = []
    
    for slot in available_slots:
        slot_start, slot_end = slot
        
        # Calculate the duration of the slot
        slot_duration = slot_end - slot_start
        
        # Check if the slot is large enough to accommodate the mock event
        if slot_duration >= timedelta(minutes=event_duration_minutes):
            # Create a mock event of the specified duration
            mock_event = Event()
            mock_event.begin = slot_start
            mock_event.end = slot_start + timedelta(minutes=event_duration_minutes)
            mock_event.name = "Mock Event"
            allocated_events.append(mock_event)
    
    return allocated_events

# Load the ICS file
ics_file_path = 'tasks.ics'  # Change this to the path of your ICS file
with open(ics_file_path, 'r') as f:
    calendar = Calendar(f.read())

# Convert events to a list
events = list(calendar.events)

# Sort events by start time to ensure correct order
events.sort(key=lambda e: e.begin)

# Find available slots
available_slots = find_available_slots(events, min_gap_minutes=30, start_hour=8, end_hour=18)

# Print available slots
print("Available slots:")
for slot in available_slots:
    print(f"Available slot from {slot[0]} to {slot[1]}")

# Allocate mock events to available slots
allocated_events = allocate_mock_events(available_slots, event_duration_minutes=60)

# Print allocated mock events
print("\nAllocated mock events:")
for event in allocated_events:
    print(f"Mock Event scheduled from {event.begin} to {event.end}")
