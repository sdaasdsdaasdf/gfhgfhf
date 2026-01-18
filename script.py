
import requests
import time
import json
import os

# ================= CONFIG =================

# List of accounts: each with its own API key and corresponding workflow_id
ACCOUNTS = [
    {
        "api_key": "app-v2ovIqnFcE61Q7RL9xNCc3E8",
        "workflow_id": "74882943574149153"
    },
    {
        "api_key": "app-6m1rrQ0Ks8wFROWfReN27TU3",
        "workflow_id": "73760693447041818"   # ID for this account's task
    },
    {
        "api_key": "app-SptQ2A4jydSH0MuYxMtwNiZD",
        "workflow_id": "74379789402461215"   # ID for this account's task
    },
    {
        "api_key": "app-iz8OTORZdNSTvgUPp0jTvWcP",
        "workflow_id": "74382096903062559"   #n ID for this account's task
    },
    {
        "api_key": "app-SpaiDiUoKGhTLV880maRjqNm",
        "workflow_id": "74385592853704737"   #n ID for this account's task
    },
    {
        "api_key": "app-i9YgKcmfMU69vuuV0AHoU1zC",
        "workflow_id": "74386969176816673"   #n ID for this account's task
    },
    {
        "api_key": "app-lquHuNmbsdFduEJv9S0KUxR7",
        "workflow_id": "74726484103428129"   #n ID for this account's task
    },
    {
        "api_key": "app-XVC2qAjXsIKFtCRvwxQmGqgM",
        "workflow_id": "74727099724496673"   #n ID for this account's task
    }
]

# File to track usage (count per API key)
USAGE_FILE = "api_key_usage.json"

# Delay between triggers (seconds) — to avoid rate limiting
DELAY_BETWEEN = 30

# Base API URL
BASE_URL = "https://api.browseract.com/v2"

# ==========================================

def load_usage():
    """Load or initialize usage counts from JSON file"""
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, 'r') as f:
            data = json.load(f)
            # Ensure all current keys are in the file
            for account in ACCOUNTS:
                key = account["api_key"]
                if key not in data:
                    data[key] = 0
            return data
    else:
        # Initialize with 0 for each API key
        return {acc["api_key"]: 0 for acc in ACCOUNTS}

def save_usage(usage_data):
    """Save updated counts to JSON file"""
    with open(USAGE_FILE, 'w') as f:
        json.dump(usage_data, f, indent=2)
    print(f"Usage saved to {USAGE_FILE}")

def get_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

def trigger_task(api_key, workflow_id):
    url = f"{BASE_URL}/workflow/run-task"
    headers = get_headers(api_key)
    payload = {
        "workflow_id": workflow_id,
        "save_browser_data": True
        # No input_parameters, profile_id, callback_url
    }

    print(f"Triggering task for key ending ...{api_key[-6:]} with workflow_id {workflow_id}")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in (200, 201):
            result = response.json()
            print("Success! Response:")
            print(json.dumps(result, indent=2))
            return True
        else:
            print("Error Response:")
            print(response.text)
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

# Main logic
usage_data = load_usage()
print("Current usage:", json.dumps(usage_data, indent=2))

successful = 0
failed = 0

for account in ACCOUNTS:
    api_key = account["api_key"]
    workflow_id = account["workflow_id"]
    
    success = trigger_task(api_key, workflow_id)
    
    if success:
        current_count = usage_data.get(api_key, 0)
        usage_data[api_key] = current_count + 1
        successful += 1
        print(f"Usage updated for key ...{api_key[-6:]} → {usage_data[api_key]} uses")
    else:
        failed += 1
    
    # Delay between accounts
    if account != ACCOUNTS[-1]:
        print(f"Waiting {DELAY_BETWEEN} seconds...")
        time.sleep(DELAY_BETWEEN)

# Save updated counts
save_usage(usage_data)

# Final summary
print("\n" + "=" * 60)
print("Summary:")
print(f"  Successful triggers: {successful}")
print(f"  Failed / errored: {failed}")
print(f"  Total accounts processed: {len(ACCOUNTS)}")
print("Final usage:", json.dumps(usage_data, indent=2))
print("=" * 60)

print("\nDone! Run again anytime to trigger more.")
