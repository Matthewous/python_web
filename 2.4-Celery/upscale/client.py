import requests
import time


response = requests.post("http://127.0.0.1:5000/upscale", files={"image_1": open("lama_300px.png", "rb")})

response_data = response.json()
print(response_data)
task_id = response_data.get("task_id")
print(task_id)

while True:
    resp = requests.get(f"http://127.0.0.1:5000/tasks/{task_id}")
    print(resp.json())
    time.sleep(25)
    if resp.json()["status"] == "SUCCESS":
        print("ok")
        break

file = resp.json().get("file_link")
print(file)
resp = requests.get(f"http://127.0.0.1:5000/processed/{file}")
print(resp.content)