import requests
import json

class ComparableAnalysisAgent:
    def __init__(self, base_url="https://datacatalog.cookcountyil.gov/resource/uzyt-m557.json", class_filters=None, max_rows=1000):
        self.base_url = base_url
        self.class_filters = class_filters or ["203", "205", "207", "234", "278"]
        self.max_rows = max_rows
        self.valid_data = []  # will be set after validation

    def fetch_data(self):
        print("[INFO] Fetching property data...")
        try:
            params = {
                "$limit": self.max_rows
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
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
            prop_class = item.get("class", "").upper()
            all_classes.add(prop_class)
            if prop_class in self.class_filters:
                filtered.append(item)
        print(f"[DEBUG] Found Property Class Codes: {sorted(all_classes)}")
        print(f"[SUCCESS] Found {len(filtered)} industrial properties")
        return filtered

    def validate_records(self, records):
        print("[INFO] Validating required fields...")
        required_fields = ["pin", "class", "township_name", "certified_tot"]
        valid = []
        for rec in records:
            if all(field in rec for field in required_fields):
                valid.append(rec)
        print(f"[INFO] {len(valid)} valid records after field check")
        self.valid_data = valid  
        return valid

    def find_comparables(self, target_pin, records=None):
        print(f"[INFO] Finding comparables for PIN: {target_pin}")
        records = records or self.valid_data

        target = next((item for item in records if item.get("pin") == target_pin), None)

        if not target:
            print("[ERROR] Target property not found.")
            return []

        target_class = target.get("class", "").upper()
        target_township = target.get("township_name", "").upper()
        try:
            target_value = float(target.get("certified_tot", 0))
        except:
            print("[ERROR] Invalid certified_tot value for target.")
            return []

        lower_bound = target_value * 0.8
        upper_bound = target_value * 1.2

        comparables = []
        for item in records:
            if item.get("pin") == target_pin:
                continue
            if item.get("class", "").upper() == target_class and item.get("township_name", "").upper() == target_township:
                try:
                    value = float(item.get("certified_tot", 0))
                    if lower_bound <= value <= upper_bound:
                        comparables.append(item)
                except:
                    continue

        if comparables:
            print(f"[SUCCESS] Found {len(comparables)} comparable properties")
            return comparables

        print("[INFO] No comparables found. Retrying with wider range ±30% (ignoring township)...")
        lower_bound = target_value * 0.7
        upper_bound = target_value * 1.3

        for item in records:
            if item.get("pin") == target_pin:
                continue
            if item.get("class", "").upper() == target_class:
                try:
                    value = float(item.get("certified_tot", 0))
                    if lower_bound <= value <= upper_bound:
                        comparables.append(item)
                except:
                    continue

        print(f"[FALLBACK] Found {len(comparables)} comparables with wider range")
        return comparables

if __name__ == "__main__":
    agent = ComparableAnalysisAgent()
    raw_data = agent.fetch_data()

    if raw_data:
        industrial_data = agent.filter_industrial_properties(raw_data)
        valid_data = agent.validate_records(industrial_data)

        if valid_data:
            sample_pin = valid_data[0]["pin"]
            comparables = agent.find_comparables(sample_pin)

            print("\n[COMPARABLES]")
            for comp in comparables[:5]:  
                print(json.dumps(comp, indent=2))
        else:
            print("[INFO] No valid industrial property data to analyze.")
    else:
        print("[INFO] No data fetched.")
