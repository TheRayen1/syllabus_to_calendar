import parser
import json 

def json_to_calendar(output):
    course_name = input("Please enter Course Name: ")
    data = json.loads(output)
    calendar_events = []
    
    for assignment in data["assignments"]:
        # Convert MM/DD/YYYY to YYYY-MM-DD
        due_date = assignment["due_date"]
        year = due_date.split('/')[2]
        month = due_date.split('/')[0]
        day = due_date.split('/')[1]
        iso_date = f"{year}-{month}-{day}"
        
        event = {
            "summary": f"{course_name}: {assignment['assignment_name']}",
            "start": {
                "dateTime": f"{iso_date}T23:00:00",  # 5 PM default
                "timeZone": "America/New_York"
            },
            "end": {
                "dateTime": f"{iso_date}T23:59:00",  # 1 hour duration
                "timeZone": "America/New_York"
            }
        }
        calendar_events.append(event)
    
    return json.dumps(calendar_events, indent=2)

output = parser.parse()
result = json_to_calendar(output)
print(result)
