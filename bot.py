import os
from flask import Flask

# Initialisation de l'application Flask
app = Flask(__name__)

# Route d'exemple
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    # Utiliser la variable d'environnement 'PORT' fournie par Render ou un port par défaut (10000)
    port = int(os.environ.get('PORT', 10000))  # Si Render fournit une variable 'PORT', on l'utilise.
    print(f"Le bot écoute sur le port {port}")  # Afficher le port où l'application écoute
    app.run(host='0.0.0.0', port=port)  # Écouter sur toutes les interfaces réseau (0.0.0.0)
