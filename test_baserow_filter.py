"""Quick test to find the correct Baserow filter syntax for single_select fields."""
import requests
import json

BASE_URL = "https://api.baserow.io"
TOKEN = "GfbLXGGgKcpIqY6dElV19wigYIAFKWst"
TABLE_LEADS = 1009952

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# Approach 1: JSON filters with field name (user_field_names=true)
print("--- Approach 1: JSON filters with field name 'status' ---")
filters_json = json.dumps({
    "filter_type": "AND",
    "filters": [{"type": "single_select_equal", "field": "status", "value": "Qualified"}]
})
resp = requests.get(
    f"{BASE_URL}/api/database/rows/table/{TABLE_LEADS}/",
    headers=headers,
    params={"user_field_names": "true", "size": 1, "filters": filters_json}
)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    print(f"Count: {resp.json().get('count')}")
else:
    print(f"Error: {resp.text[:300]}")

# Approach 2: Old-style filter with field ID and single_select_equal
print("\n--- Approach 2: filter__field_8860282__single_select_equal ---")
resp2 = requests.get(
    f"{BASE_URL}/api/database/rows/table/{TABLE_LEADS}/",
    headers=headers,
    params={"user_field_names": "true", "size": 1, "filter__field_8860282__single_select_equal": "Qualified"}
)
print(f"Status: {resp2.status_code}")
if resp2.status_code == 200:
    print(f"Count: {resp2.json().get('count')}")
else:
    print(f"Error: {resp2.text[:300]}")

# Approach 3: Old-style filter with field ID and equal + option ID
print("\n--- Approach 3: filter__field_8860282__equal with option ID ---")
resp3 = requests.get(
    f"{BASE_URL}/api/database/rows/table/{TABLE_LEADS}/",
    headers=headers,
    params={"user_field_names": "true", "size": 1, "filter__field_8860282__equal": "6407609"}
)
print(f"Status: {resp3.status_code}")
if resp3.status_code == 200:
    print(f"Count: {resp3.json().get('count')}")
else:
    print(f"Error: {resp3.text[:300]}")

# Approach 4: Old-style filter with single_select_equal + option value string
print("\n--- Approach 4: filter__field_8860282__single_select_equal with option value ---")
resp4 = requests.get(
    f"{BASE_URL}/api/database/rows/table/{TABLE_LEADS}/",
    headers=headers,
    params={"user_field_names": "true", "size": 1, "filter__field_8860282__single_select_equal": "6407609"}
)
print(f"Status: {resp4.status_code}")
if resp4.status_code == 200:
    print(f"Count: {resp4.json().get('count')}")
else:
    print(f"Error: {resp4.text[:300]}")
