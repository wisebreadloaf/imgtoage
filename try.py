import json
import base64
import requests
import subprocess

url = "http://localhost:5000/predictions"
headers = {"Content-Type": "application/json"}
data = {
    "input": {
        "image": "https://replicate.delivery/mgxm/806bea64-bb51-4c8a-bf4d-15602eb60fdd/1287.jpg",
        "target_age": "default",
    }
}

response = requests.post(url, headers=headers, json=data)
if response.status_code == 200:
    with open("output.json", "w") as f:
        json.dump(response.json(), f)
    print("Response saved to output.json")
else:
    print(f"Request failed with status code: {response.status_code}")
with open("output.json", "r") as file:
    data = json.load(file)

output_value = data.get("output")
base64_gif = output_value.split(",")[1]
gif_data = base64.b64decode(base64_gif)
with open("output.gif", "wb") as f:
    f.write(gif_data)

command = ["kitty", "+kitten", "icat", "./output.gif"]
result = subprocess.run(command, capture_output=True, text=True)

if result.returncode == 0:
    print("Command executed successfully.")
    print(result.stdout)
else:
    print(f"Command failed with return code {result.returncode}.")
    print(result.stderr)
