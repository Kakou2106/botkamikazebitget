import ccxt
import json
import time
import requests
from datetime import datetime
import os
from flask import Flask
from threading import Thread
from waitress import serve  # Importation de Waitress

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

# --- Fonction pour obtenir le prix d'un token ---
def obtenir_prix(symbole):
    try:
        bitget = init_bitget()
        ticker = bitget.fetch_ticker(symbole)
        return ticker["last"]  # Retourne le dernier prix
    except Exception as e:
        log(f"❌ Erreur lors de la récupération du prix de {symbole}: {e}")
        return None

# --- Fonction pour acheter avec USDT ---
def acheter_avec_usdt(symbole, montant_usdt):
    try:
        # Récupérer le prix actuel du token
        prix_cryptos = obtenir_prix(symbole)
        if prix_cryptos is None:
            log(f"❌ Impossible de récupérer le prix de {symbole}.")
            return
        
        # Calculer la quantité à acheter avec le montant en USDT
        quantite = montant_usdt / prix_cryptos
        
        # Créer l'ordre d'achat avec le prix et la quantité
        bitget = init_bitget()
        response = bitget.create_market_buy_order(symbol=symbole, amount=montant_usdt)  # Achat en utilisant le montant total en USDT
        
        # Vérification de la réponse de l'API
        if response['status'] == 'success':
            log(f"🟢 Achat de {montant_usdt} USDT de {symbole} effectué.")
        else:
            log(f"❌ Erreur lors de l'achat de {symbole}: {response['message']}")
    except Exception as e:
        log(f"❌ Erreur lors de l'achat de {symbole}: {str(e)}")

# --- Stratégie Kamikaze ---
def acheter_memecoins():
    # Liste des mémecoins à analyser
    coins = ['PEPE/USDT', 'DOGE/USDT', 'SHIB/USDT', 'FLOKI/USDT']
    
    # Montant à investir dans chaque coin (en USDT)
    montant_par_coin = 2  # 2 USDT par coin

    # Boucle pour acheter chaque coin
    for coin in coins:
        log(f"📊 Prix actuel {coin} = {obtenir_prix(coin)} USDT")
        log(f"🟢 Achat réel de {montant_par_coin} USDT de {coin}")
        acheter_avec_usdt(coin, montant_par_coin)

    log("✅ Analyse terminée. Reprise dans 5 min...")

# --- Lancement du bot avec Waitress (Windows) ---
if __name__ == "__main__":
    log("🚀 Démarrage du serveur Flask avec Waitress")
    Thread(target=lambda: serve(app, host='0.0.0.0', port=port)).start()  # Utilisation de Waitress pour déployer l'application
    while True:
        acheter_memecoins()  # Exécuter les achats de memecoins
        time.sleep(300)  # 5 minutes

