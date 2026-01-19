import requests
import time
import json
import os

# ================= CONFIG =================

ACCOUNTS = [
    {
        "api_key": "app-9U0gzAvCsHJ1gwM2UGZJLmny",
        "workflow_id": ["74940283357027617", "74940015248725025"]
    },
    {
        "api_key": "app-v2ovIqnFcE61Q7RL9xNCc3E8",
        "workflow_id": ["74883143512427809", "74882943574149153"]
    },
    {
        "api_key": "app-6m1rrQ0Ks8wFROWfReN27TU3",
        "workflow_id": ["74881209860270367", "73760693447041818"]
    },
    {
        "api_key": "app-SptQ2A4jydSH0MuYxMtwNiZD",
        "workflow_id": ["74379789402461215", "75031256519044639"]
    },
    {
        "api_key": "app-iz8OTORZdNSTvgUPp0jTvWcP",
        "workflow_id": ["74382096903062559", "75031511837150753"]
    },
    {
        "api_key": "app-SpaiDiUoKGhTLV880maRjqNm",
        "workflow_id": ["75032101692608289", "74385592853704737"]
    },
    {
        "api_key": "app-i9YgKcmfMU69vuuV0AHoU1zC",
        "workflow_id": ["75033249562138911", "74386969176816673"]
    },
    {
        "api_key": "app-lquHuNmbsdFduEJv9S0KUxR7",
        "workflow_id": ["75033491367960607", "74726484103428129"]
    },
    {
        "api_key": "app-XVC2qAjXsIKFtCRvwxQmGqgM",
        "workflow_id": ["75033647975217441", "74727099724496673"]
    }
]

USAGE_FILE = "api_key_usage.json"

FIRST_TO_SECOND_DELAY = 5     # seconds
ACCOUNT_TO_ACCOUNT_DELAY = 10 # seconds

BASE_URL = "https://api.browseract.com/v2"

# ==========================================

def load_usage():
    if os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "r") as f:
            data = json.load(f)
        for acc in ACCOUNTS:
            data.setdefault(acc["api_key"], 0)
        return data
    return {acc["api_key"]: 0 for acc in ACCOUNTS}

def save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"\nUsage saved → {USAGE_FILE}")

def get_headers(api_key):
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

def trigger_task(api_key, workflow_id):
    url = f"{BASE_URL}/workflow/run-task"
    payload = {
        "workflow_id": workflow_id,
        "save_browser_data": True
    }

    print(f"\nTriggering workflow {workflow_id} using key ...{api_key[-6:]}")

    try:
        r = requests.post(
            url,
            headers=get_headers(api_key),
            json=payload,
            timeout=30
        )

        print(f"Status: {r.status_code}")

        if r.status_code in (200, 201):
            print("✔ Success")
            return True
        else:
            print("✖ Failed response:")
            print(r.text)
            return False

    except requests.exceptions.RequestException as e:
        print(f"✖ Request error: {e}")
        return False

# ================= MAIN =================

usage_data = load_usage()
print("Starting usage:", json.dumps(usage_data, indent=2))

successful = 0
failed = 0

for acc_index, account in enumerate(ACCOUNTS, start=1):
    api_key = account["api_key"]
    workflow_ids = account["workflow_id"]

    print("\n==============================")
    print(f"Account {acc_index}/{len(ACCOUNTS)}")
    print("==============================")

    for wf_index, workflow_id in enumerate(workflow_ids):
        ok = trigger_task(api_key, workflow_id)

        if ok:
            usage_data[api_key] += 1
            successful += 1
            print(f"Usage → {usage_data[api_key]}")
        else:
            failed += 1

        if wf_index == 0:
            print(f"Waiting {FIRST_TO_SECOND_DELAY}s before next workflow...")
            time.sleep(FIRST_TO_SECOND_DELAY)

    if acc_index < len(ACCOUNTS):
        print(f"Waiting {ACCOUNT_TO_ACCOUNT_DELAY}s before next account...")
        time.sleep(ACCOUNT_TO_ACCOUNT_DELAY)

save_usage(usage_data)

print("\n======================================")
print("FINAL SUMMARY")
print("======================================")
print(f"Successful calls : {successful}")
print(f"Failed calls     : {failed}")
print(f"Accounts total   : {len(ACCOUNTS)}")
print("Final usage:", json.dumps(usage_data, indent=2))
print("======================================")
print("DONE.")
