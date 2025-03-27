import os
import json
import requests
from datetime import datetime

def fetch_iocs(url, filename):
    # ...existing code...
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            save_json(data, filename)
            print(f"[+] Successfully saved {filename}")
        else:
            print(f"[-] Failed to fetch {filename} (HTTP {response.status_code})")
    except requests.RequestException as e:
        print(f"[-] Error fetching {filename}: {e}")

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
    # ...existing code...
    ioc_dir = "iocs"
    os.makedirs(ioc_dir, exist_ok=True)

    sources = {
        "abuse_threatfox": "https://threatfox.abuse.ch/export/json/recent/",
        "abuse_urlhaus": "https://urlhaus.abuse.ch/downloads/json/",
        "cisa_known_vulns": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    }

    for name, url in sources.items():
        filename = os.path.join(ioc_dir, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.json")
        fetch_iocs(url, filename)

if __name__ == "__main__":
    main()

# import os
# import json
# import requests
# from datetime import datetime

# def fetch_iocs(url, filename):
#     try:
#         response = requests.get(url, timeout=10)
#         if response.status_code == 200:
#             data = response.json()
#             save_json(data, filename)
#             print(f"[+] Successfully saved {filename}")
#         else:
#             print(f"[-] Failed to fetch {filename} (HTTP {response.status_code})")
#     except requests.RequestException as e:
#         print(f"[-] Error fetching {filename}: {e}")

# def save_json(data, filename):
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(data, f, indent=4)

# def main():
#     # Directory to store IOCs
#     ioc_dir = "iocs"
#     os.makedirs(ioc_dir, exist_ok=True)

#     # IOC sources
#     sources = {
#         "abuse_threatfox": "https://threatfox.abuse.ch/export/json/recent/",
#         "abuse_urlhaus": "https://urlhaus.abuse.ch/downloads/json/",
#         "cisa_known_vulns": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
#     }

#     # Fetch IOCs
#     for name, url in sources.items():
#         filename = os.path.join(ioc_dir, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.json")
#         fetch_iocs(url, filename)

# if __name__ == "__main__":
#     main()
