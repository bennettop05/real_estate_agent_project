import requests
import json
import time
from urllib.parse import urlencode

class APIDiscoveryAgent:
    def __init__(self, base_url="https://datacatalog.cookcountyil.gov/resource/nj4t-kc8j.json", max_rows=1000):
        self.base_url = base_url
        self.max_rows = max_rows

    def get_sample_data(self):
        
        print("[INFO] Fetching sample data...")
        params = {
            "$limit": self.max_rows
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"[SUCCESS] Retrieved {len(data)} records")
            return data
        except requests.exceptions.HTTPError as e:
            print(f"[HTTP ERROR] {e}")
        except requests.exceptions.RequestException as e:
            print(f"[REQUEST ERROR] {e}")
        except Exception as e:
            print(f"[ERROR] {e}")
        return []

    def analyze_fields(self, data):
        print("[INFO] Analyzing fields...")
        field_types = {}
        for entry in data:
            for key, value in entry.items():
                dtype = type(value).__name__
                if key not in field_types:
                    field_types[key] = set()
                field_types[key].add(dtype)
        for key, types in field_types.items():
            print(f"- {key}: {', '.join(types)}")
        return field_types

    def detect_rate_limit(self):
        
        print("[INFO] Checking rate limit headers...")
        try:
            response = requests.get(self.base_url, params={"$limit": 1})
            response.raise_for_status()
            headers = response.headers
            limit_info = {
                "X-SODA-LIMIT-REMAINING": headers.get("X-SODA-LIMIT-REMAINING"),
                "X-SODA-LIMIT-REQUESTS-LEFT": headers.get("X-SODA-LIMIT-REQUESTS-LEFT")
            }
            print(f"[INFO] Rate Limit Info: {limit_info}")
            return limit_info
        except Exception as e:
            print(f"[ERROR] {e}")
            return {}

if __name__ == "__main__":
    agent = APIDiscoveryAgent()
    sample = agent.get_sample_data()
    if sample:
        agent.analyze_fields(sample)
        agent.detect_rate_limit()
