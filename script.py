import os
import json
import requests
from datetime import datetime

def fetch_iocs(url):
    # ...existing code...
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[-] Failed to fetch IOCs (HTTP {response.status_code})")
            return []
    except requests.RequestException as e:
        print(f"[-] Error fetching IOCs: {e}")
        return []

def save_json(data, filename):
    # Load existing data if the file exists
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    # Merge and deduplicate data
    if isinstance(existing_data, list) and isinstance(data, list):
        combined_data = {json.dumps(entry, sort_keys=True): entry for entry in existing_data + data}
        deduplicated_data = list(combined_data.values())
    else:
        deduplicated_data = data  # Handle non-list JSON structures

    # Save the merged and deduplicated data
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(deduplicated_data, f, indent=4)

def main():
    # Directory to store the consolidated IOCs
    ioc_file = "iocs.json"

    # IOC sources
    sources = {
        "abuse_threatfox": "https://threatfox.abuse.ch/export/json/recent/",
        "abuse_urlhaus": "https://urlhaus.abuse.ch/downloads/json/",
        "cisa_known_vulns": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    }

    # Fetch and save IOCs
    all_iocs = []
    for name, url in sources.items():
        iocs = fetch_iocs(url)
        if iocs:
            all_iocs.extend(iocs)

    save_json(all_iocs, ioc_file)

if __name__ == "__main__":
    main()
