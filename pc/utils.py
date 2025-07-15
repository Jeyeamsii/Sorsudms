import jwt
import requests
import time
from django.conf import settings

def generate_access_token():
    # Define the JWT payload
    now = int(time.time())
    payload = {
        'iss': settings.DOCUSIGN_INTEGRATION_KEY,
        'sub': settings.DOCUSIGN_USER_ID,
        'iat': now,
        'exp': now + 3600,  # Token valid for 1 hour
        'aud': 'account.docusign.com',
        'scope': 'signature'
    }

    # Encode the JWT with your private key
    private_key = settings.DOCUSIGN_PRIVATE_KEY
    encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')

    # Request an access token
    url = 'https://account.docusign.com/oauth/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        'assertion': encoded_jwt
    }
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception('Failed to obtain access token: ' + response.text)