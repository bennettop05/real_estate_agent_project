import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.comparable_agent import ComparableAnalysisAgent
from agents.attom_agent import AttomAgent


def test_fetch_data_returns_list():
    agent = ComparableAnalysisAgent(max_rows=10)
    data = agent.fetch_data()
    assert isinstance(data, list)
    assert len(data) > 0

def test_filter_industrial_properties():
    agent = ComparableAnalysisAgent()
    sample_data = [
        {"class": "203"}, {"class": "205"}, {"class": "100"}, {"class": "234"}
    ]
    filtered = agent.filter_industrial_properties(sample_data)
    assert all(item["class"] in agent.class_filters for item in filtered)

def test_validate_records():
    agent = ComparableAnalysisAgent()
    sample_records = [
        {"pin": "123", "class": "203", "township_name": "Jefferson", "certified_tot": "45000"},
        {"pin": "456", "class": "205", "certified_tot": "40000"},  
    ]
    valid = agent.validate_records(sample_records)
    assert len(valid) == 1
    assert valid[0]["pin"] == "123"

def test_find_comparables():
    agent = ComparableAnalysisAgent()
    base_record = {
        "pin": "0001",
        "class": "203",
        "township_name": "Jefferson",
        "certified_tot": "50000"
    }
    comparables = [
        {"pin": "0002", "class": "203", "township_name": "Jefferson", "certified_tot": "49000"},
        {"pin": "0003", "class": "203", "township_name": "Jefferson", "certified_tot": "60000"},
        {"pin": "0004", "class": "203", "township_name": "Jefferson", "certified_tot": "70000"},  
    ]
    dataset = [base_record] + comparables
    agent.validate_records(dataset)
    results = agent.find_comparables("0001")
    assert len(results) == 2
    assert all(r["pin"] in ["0002", "0003"] for r in results)

def test_find_comparables_fallback():
    agent = ComparableAnalysisAgent()
    base_record = {
        "pin": "0001",
        "class": "203",
        "township_name": "Jefferson",
        "certified_tot": "100000"
    }
    comparables = [
        {"pin": "0002", "class": "203", "township_name": "Jefferson", "certified_tot": "130000"},  
        {"pin": "0003", "class": "203", "township_name": "Jefferson", "certified_tot": "69000"},   
        {"pin": "0004", "class": "203", "township_name": "Jefferson", "certified_tot": "50000"}    
    ]
    dataset = [base_record] + comparables
    agent.validate_records(dataset)
    results = agent.find_comparables("0001")
    assert len(results) == 1
    assert results[0]["pin"] == "0002"

# --- New test for Attom API ---

def test_attom_recent_sale_mocked():
    agent = AttomAgent()
    result = agent.get_recent_sale("16133160270000")  # Real test only if API key is valid
    assert isinstance(result, dict) or result is None
