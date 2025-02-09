import requests
import json, os

MAILTRAP_API_TOKEN = "8d73f9afe66d1ae3b08a823808729e92"


def send_email():
    url = "https://sandbox.api.mailtrap.io/api/send/3448761"


    headers = {
        "Authorization": f"Bearer {MAILTRAP_API_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "from": {"email": "koulodjieric16@gmail.com", "name": "Data World"},
        "to": [{"email": "donaerickoulodji@gmail.com"}],  # Remplace avec ton email test
        "subject": "Test API Mailtrap",
        "text": """Je suis roméo houssou , j'aimerais que vous m'assister pour ma création 
        d'un modèle de machine learning.""",
        "category": "Test"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("✅ Email envoyé avec succès !")
    else:
        print(f"❌ Erreur {response.status_code}: {response.text}")

# Exécuter l'envoi
send_email()

