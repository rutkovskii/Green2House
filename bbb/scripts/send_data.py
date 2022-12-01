import requests, json
from datetime import datetime as dt
from datetime import timedelta as td


def send_sample_data_example(url):
    # Must change it to the actual IP address of the server
    # url = 'http://172.31.178.169/get_data'
    # url = 'https://6cb1-2601-180-8200-a250-8579-d8a5-2d2d-b895.ngrok.io/get_data'
    print(int(round(dt.timestamp(dt.now()-td(minutes=5)))))

    # Example Samples
    sample1 = {'user_id': 1, 'temperature': 68.3, 'humidity': 43.2, 'timestamp': int(round(dt.timestamp(dt.now()-td(minutes=5))))}
    sample2 = {'user_id': 1, 'temperature': 58.7, 'humidity': 71.5, 'timestamp': int(round(dt.timestamp(dt.now())))}

    # Pack the samples into a list
    entries_json = json.dumps([sample1, sample2])


    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, json=entries_json, headers=headers)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")


def send_samples(url,samples):
    # Pack the samples into a list
    entries_json = json.dumps(samples)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, json=entries_json, headers=headers)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")


if __name__ == '__main__':
    url = 'https://6cb1-2601-180-8200-a250-8579-d8a5-2d2d-b895.ngrok.io/get_data'
    send_sample_data_example(url)
