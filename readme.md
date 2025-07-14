Video Demo - https://drive.google.com/file/d/1m4RKKaPzMPVcfTODGMo1Bl702A5Cpk0x/view?usp=sharing
# 🏠 Real Estate Comparable Analysis Agent

This project is an intelligent agent that fetches Cook County (Illinois) property data via public APIs and performs **comparable analysis** for **industrial real estate**.

It helps identify properties similar in type, location, and value, automating due diligence for investors or analysts.

---

## 🚀 Features

- 📦 Fetches up to 1000 property records using Cook County public API
- 🏭 Filters **industrial property classes**
- ✅ Validates records with required fields
- 📊 Finds comparable properties based on:
  - Property class
  - Township
  - Certified total value (±20% or ±30%)
- 📄 Generates a final report in JSON
- 🧪 Includes unit tests for core functionalities

---

## 🧠 Architecture

main.py
└── agents/
└── comparable_agent.py ← core logic agent
└── tests/
└── test_sample.py ← pytest test cases
└── data/
└── final_report.json ← saved output


## 🧪 Running the App

### ✅ 1. Install dependencies

```bash
pip install -r requirements.txt
(or manually just use requests, pytest if not using a requirements.txt)

✅ 2. Run the main script
python main.py
✅ 3. Run tests
pytest
📁 Sample Output
The final report is saved to:
data/final_report.json
Sample JSON includes:

subject_property

num_comparables

comparables: list of similar industrial properties

avg_certified_value

🛠 Technologies Used
Python 3.10+

Public Cook County Property API

Pytest (for testing)
