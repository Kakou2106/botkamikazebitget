import ccxt
import json
import time
import requests
from datetime import datetime
import os
from flask import Flask
from threading import Thread

# --- Configuration Flask ---
app = Flask(__name__)
port = int(os.environ.get("PORT", 10000))

@app.route('/')
def home():
    return '✅ Bot Kamikaze en ligne et prêt !'

# --- Logger + Telegram ---
def log(msg):
    print(msg)
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {msg}\n")
    if "Achat simulé" in msg or "Vente automatique" in msg:
        send_telegram(msg)

def send_telegram(message):
    try:
        config = load_config()
        token = config.get("telegram_token")
        chat_id = config.get("telegram_chat_id")
        if not token or not chat_id:
            log("❌ Token Telegram ou Chat ID manquant dans config.json")
            return
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}
        requests.post(url, data=payload)
    except Exception as e:
        log(f"❌ Erreur Telegram : {e}")

# --- Chargement de la config ---
def load_config():
    config_path = "config.json"
    if not os.path.exists(config_path):
        log("❌ Fichier config.json introuvable.")
        exit(1)
    with open(config_path, "r") as f:
        return json.load(f)

# --- Initialisation de Bitget ---
def init_bitget():
    config = load_config()
    return ccxt.bitget({
        'apiKey': config.get("bitget_api_key"),
        'secret': config.get("bitget_api_secret")
    })

# --- Stratégie Kamikaze ---
def get_memecoins():
    return ["PEPE/USDT", "DOGE/USDT", "SHIB/USDT", "FLOKI/USDT", "HOGE/USDT", "KISHU/USDT"]

def should_buy(symbol):
    return True

def should_sell(entry, current):
    return ((current - entry) / entry) < -0.10

# --- Fonction principale ---
def main():
    log("🚀 Démarrage du bot Kamikaze")
    config = load_config()
    bitget = init_bitget()
    memecoins = get_memecoins()

    for symbol in memecoins:
        try:
            ticker = bitget.fetch_ticker(symbol)
            price = ticker["last"]
            log(f"📊 Prix actuel {symbol} = {price}")
            if should_buy(symbol):
                log(f"🟢 Achat simulé de {symbol} pour 10 USDT")
        except Exception as e:
            log(f"❌ Erreur récupération {symbol} : {e}")

    held = {"PEPE/USDT": {"entry": 0.000001, "current": 0.00000085}}
    for symbol, data in held.items():
        if should_sell(data["entry"], data["current"]):
            log(f"🔻 Vente automatique simulée de {symbol} à perte (>10%)")

    log("✅ Analyse terminée. Reprise dans 5 min...\n")

# --- Lancement continu ---
if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()
    while True:
        main()
        time.sleep(300)  # 5 minutes
