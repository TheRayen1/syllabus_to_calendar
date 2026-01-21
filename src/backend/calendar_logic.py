import json
import os
import logging
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_oauth_flow(redirect_uri):
    """Create OAuth flow for web application"""
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    return flow


def get_authorization_url(redirect_uri):
    """Get the URL to redirect user to for Google OAuth"""
    flow = get_oauth_flow(redirect_uri)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    return authorization_url, state


def exchange_code_for_credentials(code, redirect_uri):
    """Exchange authorization code for credentials"""
    flow = get_oauth_flow(redirect_uri)
    flow.fetch_token(code=code)
    return flow.credentials


def json_to_calendar(output, course_name):
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
                "dateTime": f"{iso_date}T23:00:00",
                "timeZone": "America/New_York"
            },
            "end": {
                "dateTime": f"{iso_date}T23:59:00",
                "timeZone": "America/New_York"
            }
        }
        calendar_events.append(event)
    return calendar_events


def send_to_calendar(events, credentials_dict):
    """Send events to Google Calendar using user's credentials"""
    logger.info(f"=== SEND TO CALENDAR START ===")
    logger.info(f"Number of events to add: {len(events)}")

    creds = Credentials(
        token=credentials_dict['token'],
        refresh_token=credentials_dict.get('refresh_token'),
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict['scopes']
    )
    logger.info("Credentials created successfully")

    service = build('calendar', 'v3', credentials=creds)
    logger.info("Calendar service built successfully")

    added_events = []
    for i, event in enumerate(events):
        logger.info(f"Adding event {i+1}: {event}")
        try:
            result = service.events().insert(calendarId='primary', body=event).execute()
            logger.info(f"Event added successfully: {result.get('summary')} - {result.get('htmlLink')}")
            added_events.append(result.get('summary'))
        except Exception as e:
            logger.error(f"Failed to add event: {e}")

    logger.info(f"=== SEND TO CALENDAR END === Added {len(added_events)} events")
    return added_events