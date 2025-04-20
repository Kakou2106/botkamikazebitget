
import json
import time
import requests
from datetime import datetime
import os

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
        response = requests.post(url, data=payload)
        
        if response.status_code != 200:
            log(f"❌ Erreur HTTP lors de l'envoi du message : {response.status_code} - {response.text}")
        else:
            log("✅ Message envoyé avec succès.")
    except Exception as e:
        log(f"❌ Erreur envoi Telegram : {e}")


# Fonction pour écrire dans les logs
# Fonction pour écrire dans les logs et afficher à l'écran
def log(msg):
    msg = msg.encode('utf-8', 'replace').decode('utf-8')
    print(msg)
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {msg}\n")

    # Exemple : envoie certains messages sur Telegram
    if "Achat simulé" in msg or "Vente automatique" in msg:
        send_telegram(msg)

# Fonction pour charger la config
def load_config():
    config_path = "config.json"
    if not os.path.exists(config_path):
        log("❌ Fichier config.json introuvable. Créez-le avant de lancer le bot.")
        exit(1)
    with open(config_path, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            log("❌ Erreur dans le fichier config.json (JSON invalide).")
            exit(1)

# Liste simulée de memecoins
def get_memecoins():
    return ["PEPE", "TURBO", "DOGE", "SHIB"]

def should_buy(symbol):
    return True

def should_sell(entry_price, current_price):
    return ((current_price - entry_price) / entry_price) < -0.10

def main():
    log("🚀 Démarrage du bot kamikaze.")
    config = load_config()
    usdt_balance = 100
    memecoins = get_memecoins()

    for coin in memecoins:
        if should_buy(coin) and usdt_balance >= 10:
            log(f"🟢 Achat simulé de {coin} pour 10 USDT")
            usdt_balance -= 10

    held_positions = {"PEPE": {"entry": 0.000001, "current": 0.00000085}}

    for symbol, data in held_positions.items():
        if should_sell(data["entry"], data["current"]):
            log(f"🔻 Vente automatique simulée de {symbol} à perte (>10%)")

    log("✅ Analyse terminée. En attente 5 minutes...\n")

if __name__ == "__main__":
    log("🟡 Lancement du bot...")
    while True:
        main()
        time.sleep(300)
