'''
Tests for jwt flask app.
'''
import os
import json
import pytest

import main

SECRET = 'myjwtsecret'
TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2ODkyMDgzNDMsIm5iZiI6MTY4Nzk5ODc0MywiZW1haWwiOiJtci5uZ3V5ZW50cm9uZ3BodWNAZ21haWwuY29tIn0.N8d3px1OAAh_GMLH775rZW3Kd25dgeP5vUcgPIsBogY'
EMAIL = 'mr.nguyentrongphuc@gmail.com'
PASSWORD = 'mypwd'

@pytest.fixture
def client():
    os.environ['JWT_SECRET'] = SECRET
    main.APP.config['TESTING'] = True
    client = main.APP.test_client()

    yield client



def test_health(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == 'Healthy'


def test_auth(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    assert response.status_code == 200
    token = response.json['token']
    assert token is not None

def test_contents(client):
    body = {'email': EMAIL,
            'password': PASSWORD}
    response = client.post('/auth', 
                           data=json.dumps(body),
                           content_type='application/json')

    token = response.json['token']

    headers = {'Authorization': token }
    response = client.get('/contents',
                           headers=headers)

    assert response.status_code == 200
    email = response.json['email']
    assert email == EMAIL
