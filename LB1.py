import requests
import json

url_string = "https://bank.gov.ua/NBU_Exchange/exchange_site?json&start=20241007&end=20241011&valcode=usd"

my_response = requests.get(url_string)

print(my_response)
print(my_response.content)

response_json = json.loads(my_response.content)

print(response_json)
for item in response_json:
     print(item['rate'])
