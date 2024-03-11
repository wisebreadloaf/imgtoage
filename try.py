import json
import base64

with open('output.json', 'r') as file:
    data = json.load(file)

output_value = data.get('output')
base64_gif = output_value.split(',')[1]
gif_data = base64.b64decode(base64_gif)
with open('output.gif', 'wb') as f:
    f.write(gif_data)
