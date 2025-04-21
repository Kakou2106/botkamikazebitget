import os

port = int(os.environ.get("PORT", 10000))  # Utilise le port dynamique de Render, sinon 10000 par défaut.
app.run(host="0.0.0.0", port=port)
