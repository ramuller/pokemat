import requests
import json


class GPSControl:
    def __init__(self, gps_rest_url="http://localhost:2769"):
        self.gps_rest_url = gps_rest_url


    def get_status(self):
        try:
            response = requests.get(f"{self.gps_rest_url}/status")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get status. HTTP Status Code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception occurred while getting location: {e}")
            return None

    def get_speed(self):
        status = self.get_status()
        return status.get("speed_kmh", None) if status else None

    def get_running(self):
        status = self.get_status()
        return status.get("running", None) if status else None

    def set_speed(self, speed_kmh):
        try:
            response = requests.get(f"{self.gps_rest_url}/control?speed={speed_kmh}")
            if response.status_code == 200:
                return True
            else:
                print(f"Failed to set speed. HTTP Status Code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Exception occurred while setting speed: {e}")
            return False

    def start(self):
        try:
            response = requests.get(f"{self.gps_rest_url}/control?start=1")
            if response.status_code == 200:
                return True
            else:
                print(f"Failed to start GPS. HTTP Status Code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Exception occurred while starting GPS: {e}")
            return False

    def stop(self):
        try:
            response = requests.get(f"{self.gps_rest_url}/control?stop=1")
            if response.status_code == 200:
                return True
            else:
                print(f"Failed to stop GPS. HTTP Status Code: {response.status_code}")
                return False
        except Exception as e:
            print(f"Exception occurred while stopping GPS: {e}")
            return False