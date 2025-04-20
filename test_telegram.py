import requests

token = "7850068311:AAHVIOWt8YHeElK6hmflVoVf6S_KvsxSzBk"
chat_id = "7601286564"
message = "✅ Test depuis ton bot kamikaze !"

url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {"chat_id": chat_id, "text": message}

response = requests.post(url, data=payload)
print(response.status_code)
print(response.text)
