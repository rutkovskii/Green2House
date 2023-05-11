import requests
import json
from datetime import datetime as dt
from datetime import timedelta as td

from bbb_config import BBB_Config as Config
from database.database import session_scope, get_unsent_samples, mark_samples_as_sent


def send_samples_db():
    """Send the unsent samples to the server."""
    # Define the server URL
    server_url = Config.SERVER_GET_DATA_URL

    # Get the unsent samples from the database
    with session_scope() as s:
        unsent_samples = get_unsent_samples(s)
        print(1)
        # If there are unsent samples, send them to the server
        if unsent_samples:
            # Convert the samples to a JSON payload
            payload = json.dumps([sample.to_dict() for sample in unsent_samples])
            print(2)
            for attempt in range(3):
                try:
                    # Send the samples to the server in JSON format
                    print(3)
                    response = requests.post(server_url, json=payload)
                    print(4)
                    # If the server responds with a 200 status code, mark the samples as sent in the database
                    if response.status_code == 200:
                        print(5)
                        with session_scope() as s:
                            print(6)
                            mark_samples_as_sent(s, unsent_samples)
                            print(7)
                        break
                    else:
                        print(8)
                        raise Exception(
                            f"Server responded with status code {response.status_code}"
                        )

                except Exception as e:
                    print(9)
                    print(
                        f"Error sending samples to the server (attempt {attempt + 1}): {e}"
                    )

        else:
            print(10)
            # If there are no unsent samples, do not send anything to the server
            response = None

def send_sample_data_example(url):
    # Must change it to the actual IP address of the server
    # url = 'http://172.31.178.169/get_data'
    # url = 'https://6cb1-2601-180-8200-a250-8579-d8a5-2d2d-b895.ngrok.io/get_data'
    print(int(round(dt.timestamp(dt.now() - td(minutes=5)))))

    # Example Samples
    sample1 = {
        "user_id": 1,
        "temperature": 68.3,
        "humidity": 43.2,
        "timestamp": int(round(dt.timestamp(dt.now() - td(minutes=5)))),
    }
    sample2 = {
        "user_id": 1,
        "temperature": 58.7,
        "humidity": 71.5,
        "timestamp": int(round(dt.timestamp(dt.now()))),
    }

    # Pack the samples into a list
    entries_json = json.dumps([sample1, sample2])

    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    r = requests.post(url, json=entries_json, headers=headers)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")


def send_samples(url, samples):
    # Pack the samples into a list
    entries_json = json.dumps(samples)
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    r = requests.post(url, json=entries_json, headers=headers)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")


if __name__ == "__main__":
    url = "https://6cb1-2601-180-8200-a250-8579-d8a5-2d2d-b895.ngrok.io/get_data"
    send_sample_data_example(url)
