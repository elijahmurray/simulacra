import datetime
import json

def get_datetime_from_time_string(string_time):
    return datetime.datetime.strptime(string_time, '%I:%M%p').time()

def get_datetime_from_datetime_string(string_datetime):
    return datetime.datetime.strptime(string_datetime, "%Y-%m-%d %H:%M:%S")

def is_in_time_window(sim_time: datetime.datetime, plan_start_time_str: str, duration_minutes: int):
    '''
    Utility function to take plan times which are string of the form "8:00AM" and durations which are integers, and determine what plan object corresponds to the current sim time
    '''
    # Convert the plan time string to a datetime object
    plan_start_time = get_datetime_from_time_string(plan_start_time_str)
    plan_start_datetime = datetime.datetime.combine(sim_time.date(), plan_start_time)
    plan_end_datetime = plan_start_datetime + datetime.timedelta(minutes=duration_minutes)
    if plan_start_datetime <= sim_time < plan_end_datetime:
        return True
    else:
      return False

def extract_json(text):
    json_start = text.find('{')
    json_end = text.rfind('}') + 1
    json_str = text[json_start:json_end]
    return json.loads(json_str)
