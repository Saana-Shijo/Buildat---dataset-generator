#!/home/nandana/nanobot-env/bin/python3
"""
NanoBot Skill: Generate Steam Dataset as CSV
"""

import json
import subprocess
import sys
import os

def run(params):
    if isinstance(params, str):
        try:
            params = json.loads(params)
        except:
            params = {"query": params}
    
    query = params.get("query", "RPG")
    limit = params.get("limit", 10)
    
    scraper_path = os.path.join(os.path.dirname(__file__), "steam_csv_scraper.py")
    
    result = subprocess.run([
        sys.executable, scraper_path,
        "--source", "steam",
        "--query", query,
        "--limit", str(limit)
    ], capture_output=True, text=True)
    
    # Find the generated CSV file
    datasets_dir = "/home/nandana/.nanobot/workspace/datasets"
    csv_files = [f for f in os.listdir(datasets_dir) if f.startswith(f"steam_{query.replace(' ', '_')}") and f.endswith('.csv')]
    
    latest_csv = None
    if csv_files:
        latest_csv = max(csv_files, key=lambda x: os.path.getctime(os.path.join(datasets_dir, x)))
    
    return {
        "success": result.returncode == 0,
        "output": result.stdout,
        "csv_file": latest_csv,
        "csv_path": os.path.join(datasets_dir, latest_csv) if latest_csv else None,
        "query": query,
        "limit": limit
    }

def describe():
    return {
        "name": "generate-csv-dataset",
        "description": "Generate Steam game dataset as CSV file (direct output, no JSON)",
        "inputs": {"query": "Game genre (RPG, Action, Horror)", "limit": "Number of games"},
        "outputs": {"csv_file": "string", "csv_path": "string"}
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(run(sys.argv[1]), indent=2))
    else:
        print(json.dumps(describe(), indent=2))