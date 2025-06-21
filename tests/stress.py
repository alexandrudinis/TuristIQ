import requests
import time

url = "http://192.168.4.1:5000/chat"
headers = {"Content-Type": "application/json"}
payload = {"question": "Care este povestea satului Geamăna?"}

for i in range(100):
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"[{i + 1}/100] Răspuns: {response.json().get('answer')[:60]}...")
        else:
            print(f"[{i + 1}/100] Eroare: {response.status_code}")
    except Exception as e:
        print(f"[{i + 1}/100] Excepție: {e}")
    
    time.sleep(0.1)  # 100 ms
