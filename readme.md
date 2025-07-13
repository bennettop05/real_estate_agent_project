# 🏠 Real Estate Comparable Analysis Agent

This project is a smart agent system that fetches property data from Cook County's open API and finds comparable industrial real estate properties based on valuation, township, and class code.

### 🚀 Features

- Fetches up to 1000 property records from Cook County API
- Filters for industrial properties using custom class codes
- Finds comparables based on:
  - Property class
  - Township (priority)
  - Certified total value (±20%, fallback ±30%)
- Generates a report with:
  - Subject property
  - List of comparables
  - Average certified value
- Saves output to `data/final_report.json`

---

### 🛠️ Tech Stack

- Python 3
- Requests (HTTP client)
- JSON (data handling)

---

### 📦 Installation

```bash
git clone https://github.com/bennettop05/real_estate_agent_project.git
cd real_estate_agent_project
pip install -r requirements.txt
⚙️ Usage
bash
Copy
Edit
python main.py
✅ The agent will:

Fetch data

Identify industrial properties

Pick one sample property

Find comparables

Save report in data/final_report.json

📄 Sample Output
json
Copy
Edit
{
  "subject_property": { ... },
  "num_comparables": 22,
  "comparables": [...],
  "avg_certified_value": 40942.64
}
🤖 Future Enhancements
Add a Streamlit or Flask dashboard for interactive filtering

Accept custom PIN input via CLI or chatbot

Export comparables to CSV/Excel

Connect to multiple counties (multi-agent setup)