import requests

ride = {
    "PULocationID": 20,
    "DOLocationID": 60,
    "trip_distance": 55.7
}

url = 'http://localhost:9696/predict'
response = requests.post(url, json=ride)
print(response.json())
