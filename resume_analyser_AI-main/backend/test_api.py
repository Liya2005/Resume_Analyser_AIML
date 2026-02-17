import requests
import json

# Test if API is running
try:
    response = requests.get('http://localhost:5000/')
    print("API Status:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error connecting to API:", e)

# Test API info endpoint
try:
    response = requests.get('http://localhost:5000/api')
    print("API Info:", response.json())
except Exception as e:
    print("Error:", e)