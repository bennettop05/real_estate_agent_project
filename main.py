from agents.comparable_agent import ComparableAnalysisAgent
from agents.attom_agent import AttomAgent
import json
import os

def main():
    print("[STEP 1] Fetching and filtering Cook County data...")
    comp_agent = ComparableAnalysisAgent()
    raw_data = comp_agent.fetch_data()
    if not raw_data:
        print("[ERROR] No data fetched.")
        return

    filtered = comp_agent.filter_industrial_properties(raw_data)
    valid = comp_agent.validate_records(filtered)
    if not valid:
        print("[ERROR] No valid industrial records found.")
        return

    target_pin = valid[0]["pin"]
    comparables = comp_agent.find_comparables(target_pin)

    subject = [rec for rec in valid if rec["pin"] == target_pin]
    report = {
        "subject_property": subject[0] if subject else "Not found",
        "num_comparables": len(comparables),
        "comparables": comparables
    }

    certified_vals = [float(r["certified_tot"]) for r in comparables if "certified_tot" in r]
    if certified_vals:
        report["avg_certified_value"] = round(sum(certified_vals) / len(certified_vals), 2)

    print("\n[STEP 2] Enriching comparables with Attom API...")
    attom_agent = AttomAgent()

    for rec in report["comparables"]:
        pin = rec.get("pin", "")
        attom_data = attom_agent.get_recent_sale(pin)
        rec["attom_sale_amount"] = attom_data.get("sale_amount") if attom_data else "Not Found"
        rec["attom_sale_date"] = attom_data.get("sale_date") if attom_data else "N/A"

    print("\n[REPORT SUMMARY]")
    print(json.dumps(report, indent=2))

    os.makedirs("data", exist_ok=True)
    with open("data/final_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n[INFO] Report saved to data/final_report.json")

if __name__ == "__main__":
    main()
