import requests

def register_with_test_server():
    registration_url = "http://20.244.56.144/test/register"
    registration_data = {
        "companyName": "goMart",
        "ownerName": "Rahul",
        "rollNo": "1",
        "ownerEmail": "rahul@abc.edu",
        "accessCode": "sdgkhx"
    }
    
    response = requests.post(registration_url, json=registration_data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Registration failed: " + response.text)

def get_authorization_token(client_id, client_secret):
    auth_url = "http://20.244.56.144/test/auth"
    auth_data = {
        "companyName": "goMart",
        "clientID": client_id,
        "clientSecret": client_secret,
        "ownerName": "Rahul",
        "ownerEmail": "rahul@abc.edu",
        "rollNo": "1"
    }
    
    response = requests.post(auth_url, json=auth_data)
    if response.status_code == 200:
        return response.json()["access token"]
    else:
        raise Exception("Authorization failed: " + response.text)

# Register with the test server
registration_response = register_with_test_server()
client_id = registration_response["clientID"]
client_secret = registration_response["clientSecret"]

print("Client ID:", client_id)
print("Client Secret:", client_secret)

# Obtain the authorization token
access_token = get_authorization_token(client_id, client_secret)
print("Access Token:", access_token)

