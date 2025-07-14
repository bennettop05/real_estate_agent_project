import requests
import json

class DataExtractionAgent:
    def __init__(self, base_url="https://datacatalog.cookcountyil.gov/resource/uzyt-m557.json", industrial_classes=None, max_rows=1000):
        self.base_url = base_url
        self.industrial_classes = industrial_classes or ["207", "208", "209"]  # Common industrial class codes
        self.max_rows = max_rows

    def fetch_data(self):
        print("[INFO] Fetching property data...")
        try:
            params = {
                "$limit": self.max_rows
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if not data:
                print("[ERROR] No records returned")
                return []
            print(f"[SUCCESS] Fetched {len(data)} records")
            print("[DEBUG] Sample Record:\n", json.dumps(data[0], indent=2))
            return data
        except Exception as e:
            print(f"[ERROR] {e}")
            return []

    def filter_industrial_properties(self, data):
        print("[INFO] Filtering industrial properties by class codes...")
        filtered = []
        all_classes = set()

        for item in data:
            property_class = item.get("class", "").strip()
            if property_class:
                all_classes.add(property_class)
            if property_class in self.industrial_classes:
                filtered.append(item)

        print(f"[DEBUG] Found Property Class Codes: {sorted(all_classes)}")
        print(f"[SUCCESS] Found {len(filtered)} industrial properties")
        return filtered

    def validate_records(self, records):
        print("[INFO] Validating required fields...")
        required_fields = ["pin", "class", "township_name"]
        valid = []
        for rec in records:
            if all(field in rec for field in required_fields):
                valid.append(rec)
        print(f"[INFO] {len(valid)} valid records after field check")
        return valid

    def flag_outliers(self, records):
        print("[INFO] Checking for outliers in mailed_tot value...")
        suspicious = []
        for rec in records:
            try:
                value = float(rec.get("mailed_tot", 0))
                if value > 1000000 or value < 100:
                    suspicious.append(rec)
            except:
                continue
        print(f"[WARNING] {len(suspicious)} suspicious records flagged")
        return suspicious

if __name__ == "__main__":
    agent = DataExtractionAgent()
    raw_data = agent.fetch_data()

    if raw_data:
        industrial_data = agent.filter_industrial_properties(raw_data)
        valid_data = agent.validate_records(industrial_data)
        outliers = agent.flag_outliers(valid_data)

        print("\n[SUMMARY]")
        print(f"Total Fetched: {len(raw_data)}")
        print(f"Industrial Properties: {len(industrial_data)}")
        print(f"Valid Records: {len(valid_data)}")
        print(f"Outliers: {len(outliers)}")
    else:
        print("[INFO] No data fetched.")
