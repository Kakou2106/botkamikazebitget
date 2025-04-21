import json
import time
import requests
from datetime import datetime
import os
from flask import Flask

app = Flask(__name__)

# Utilise le port dynamique de Render (ou 10000 si non défini)
port = int(os.environ.get("PORT", 10000))

# Lancer l'app Flask sur le port dynamique
app.run(host="0.0.0.0", port=port)


# Fonction pour envoyer un message Telegram
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

# Logique pour déterminer si on achète un coin
def should_buy(symbol):
    return True  # Par exemple, on peut ajouter une logique ici pour chaque coin

# Logique pour déterminer si on vend un coin
def should_sell(entry_price, current_price):
    return ((current_price - entry_price) / entry_price) < -0.10

# Fonction principale du bot
def main():
    log("🚀 Démarrage du bot kamikaze.")
    config = load_config()
    usdt_balance = 100  # Solde USDT simulé
    memecoins = get_memecoins()

    # Simuler l'achat de memecoins
    for coin in memecoins:
        if should_buy(coin) and usdt_balance >= 10:
            log(f"🟢 Achat simulé de {coin} pour 10 USDT")
            usdt_balance -= 10

    # Positions détenues simulées
    held_positions = {"PEPE": {"entry": 0.000001, "current": 0.00000085}}

    # Vérification des positions pour vendre
    for symbol, data in held_positions.items():
        if should_sell(data["entry"], data["current"]):
            log(f"🔻 Vente automatique simulée de {symbol} à perte (>10%)")

    log("✅ Analyse terminée. En attente 5 minutes...\n")

# Application Flask pour le serveur
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == "__main__":
    log("🟡 Lancement du bot...")
    
    # Démarrage du bot toutes les 5 minutes
    while True:
        main()
        time.sleep(300)

    # Lancer le serveur Flask sur le port 10000
    app.run(host='0.0.0.0', port=10000)
