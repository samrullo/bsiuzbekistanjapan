import requests
from flask import current_app
def get_google_provider_cfg():
    return requests.get(current_app.config.get('GOOGLE_DISCOVERY_URL')).json()