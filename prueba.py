import requests

API_URL = "https://pobladorestringido.pythonanywhere.com"
resp = requests.get(f"{API_URL}")
print(resp)