# main.py

from agents.comparable_agent import ComparableAnalysisAgent
import json
import os

def main():
    agent = ComparableAnalysisAgent()

    # Phase 1-3 steps
    raw_data = agent.fetch_data()
    if not raw_data:
        print("[ERROR] No data fetched.")
        return

    filtered = agent.filter_industrial_properties(raw_data)
    valid = agent.validate_records(filtered)

    if not valid:
        print("[ERROR] No valid industrial records found.")
        return

    target_pin = valid[0]["pin"]  # ✅ Now this is defined after `valid`

    comparables = agent.find_comparables(target_pin)

    subject = [rec for rec in valid if rec["pin"] == target_pin]

    report = {
        "subject_property": subject[0] if subject else "Not found",
        "num_comparables": len(comparables),
        "comparables": comparables
    }

    # Add avg certified value (optional)
    certified_vals = [float(r["certified_tot"]) for r in comparables if "certified_tot" in r]
    if certified_vals:
        report["avg_certified_value"] = round(sum(certified_vals) / len(certified_vals), 2)

    # Output
    print("\n[REPORT SUMMARY]")
    print(json.dumps(report, indent=2))

    # Save to file
    os.makedirs("data", exist_ok=True)
    with open("data/final_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\n[INFO] Report saved to data/final_report.json")

if __name__ == "__main__":
    main()
