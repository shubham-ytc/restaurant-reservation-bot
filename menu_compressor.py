#Note- the scaledown ai not work well for menu compression 
import requests
import json
from provider import getMenu

api_key =""
url = "https://api.scaledown.xyz/compress/raw/"

def compressor():
    headers = {
    'x-api-key': api_key,
    'Content-Type': 'application/json'
    }
    payload = {
    "context": getMenu(),
    "prompt": "Compress the following restaurant menu while preserving all dish names, prices.",
    "model": "gpt-4o",
    "scaledown": {
    "rate": "auto" # Automatic compression rate optimization
    }
    }

    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    result = response.json()

    return result["results"]["compressed_prompt"]
    # print(result["results"]["compressed_prompt"])
    # print(result["results"]["success"])


print(compressor())
