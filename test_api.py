import requests
import json
import numpy as np

# Simulate a 50x21 Tensor (Representing an extracted sequence from FD004)
# In production, this would be loaded directly from test_FD004.txt
print("1. Booting Telemetry Extractor...")
mock_sequence = np.random.rand(50, 21).tolist()

payload = {
    "sensor_sequence": mock_sequence
}

# The API Service Endpoint
url = "http://127.0.0.1:8000/predict"

print(f"2. Pushing Array -> {url}")
try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("\n=== FASTAPI MISSION CONTROL RESPONSE ===")
        print(json.dumps(response.json(), indent=4))
        
        # Verify specific keys exist per our Schema
        if "RUL" in response.json():
            print("\n🏁 MASTER DEMO SUCCESSFUL: ALL SYSTEMS GO")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except requests.exceptions.ConnectionError:
    print("⚠️ API is offline. Ensure `uvicorn src.api_service:app --reload` is running on port 8000.")
