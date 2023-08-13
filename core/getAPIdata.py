import requests

"""
Data Fetching Functions
-----------------------

This module contains functions for fetching data from a remote API, specifically for retrieving CO2 sensor data.

Functions:
    fetch_data(url: str, api_key: str) -> dict:
        Fetches data from a given URL using the provided API key as a header.
        
        Parameters:
            url (str): The URL of the API to fetch data from.
            api_key (str): The API key used as a header in the request.
        
        Returns:
            dict: A dictionary containing the fetched data.

    get_data_co2() -> float or None:
        Retrieves the recent CO2 sensor data from a specific API.
        
        Returns:
            float or None: The CO2 sensor data value if available, otherwise None.
"""


def fetch_data(url, api_key):
    try:
        headers = {"x-api-key": f"{api_key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print("Error:", e)


def get_data_co2():
    api_url = "https://api.pulsegrow.com/devices/19635/recent-data"
    api_key = "4w7Ax75tSESR5J71vBtNhH9ADQbbAMThF0oHPEaMYFvEjBr"
    try:
        data = fetch_data(api_url, api_key)
        if data:
            return data["co2"]
    except Exception as e:
        print(f"Exception caught: {e}")
        return None
