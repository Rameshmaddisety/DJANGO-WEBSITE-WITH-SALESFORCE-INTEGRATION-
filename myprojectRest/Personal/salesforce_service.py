# salesforce_service.py

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

def get_salesforce_access_token():
    token_url = f'https://login.salesforce.com/services/oauth2/token'

    data = {
        'grant_type': 'password',
        'client_id': settings.SALESFORCE_CONSUMER_KEY,
        'client_secret': settings.SALESFORCE_CONSUMER_SECRET,
        'username': settings.SALESFORCE_USERNAME,
        'password': f'{settings.SALESFORCE_PASSWORD}{settings.SALESFORCE_SECURITY_TOKEN}'
    }

    response = requests.post(token_url, auth=HTTPBasicAuth(settings.SALESFORCE_CONSUMER_KEY, settings.SALESFORCE_CONSUMER_SECRET), data=data)
    return response.json().get('access_token')

def query_salesforce(query):
    base_url = f'https://rameshmaddisetty-dev-ed.develop.my.salesforce.com/services/data/v{settings.SALESFORCE_API_VERSION}'
    query_url = f'{base_url}/query/?q={query}'

    headers = {
        'Authorization': f'Bearer {get_salesforce_access_token()}',
        'Content-Type': 'application/json',
    }

    response = requests.get(query_url, headers=headers)
    return response.json()['records']

def create_salesforce_record(object_type, data):
    base_url = f'https://rameshmaddisetty-dev-ed.develop.my.salesforce.com/services/data/v{settings.SALESFORCE_API_VERSION}'
    create_url = f'{base_url}/sobjects/{object_type}/'

    headers = {
        'Authorization': f'Bearer {get_salesforce_access_token()}',
        'Content-Type': 'application/json',
    }

    response = requests.post(create_url, headers=headers, json=data)
    return response.json()

def update_salesforce_record(object_type,record_id, updated_data):
    access_token = get_salesforce_access_token()

    url = f'https://rameshmaddisetty-dev-ed.develop.my.salesforce.com/services/data/v{settings.SALESFORCE_API_VERSION}/sobjects/{object_type}/{record_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }

    response = requests.patch(url, headers=headers, json=updated_data)

    if response.status_code == 204:
        return 10
    else:
        raise Exception(f"Salesforce update error: {response.text}")
