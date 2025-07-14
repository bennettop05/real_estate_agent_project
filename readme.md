# 🏘️ Real Estate Comparable Analysis Agent

This project is an intelligent agent system that automates **comparable property analysis** using **Cook County open data** and the **Attom API**. It identifies similar industrial properties based on PIN and enriches the data with recent sale history for valuation insights.

---

## 🚀 Features

- ✅ Fetches & filters industrial properties from Cook County's open data
- 🧠 Identifies comparable properties based on class, township, and certified value
- 📊 Enriches each comparable with **recent sale data** from the Attom API
- 📄 Generates a full analysis report in `data/final_report.json`

---

## 📦 Project Structure

real_estate_agent_project/
│
├── agents/
│ ├── comparable_agent.py # Fetches, filters, and finds comparables
│ └── attom_agent.py # Integrates Attom API for sales data
│
├── data/
│ └── final_report.json # Auto-generated comparable analysis report
│
├── main.py # Entry point to run the complete pipeline
├── requirements.txt # All dependencies
└── README.md # This file

---

## 📊 Sample Output

Each comparable in the final report includes:

```json
{
  "pin": "13163040320000",
  "certified_tot": "37000.0",
  "attom_sale_amount": 17821,
  "attom_sale_date": "2024-09-14"
}
🔐 API Key Setup
To enable Attom API access, create a .env file:

ATTOM_API_KEY=your_attom_api_key_here
🛠️ How to Run
Install dependencies

pip install -r requirements.txt
Run the analysis

python main.py
📁 Output
The analysis report is saved at:

data/final_report.json

📌 Technologies
Python

Requests

Cook County Data API

Attom Property API

JSON

🙋‍♂️ Author
Aryan Singh
GenAI & Intelligent Agent Enthusiast
GitHub

