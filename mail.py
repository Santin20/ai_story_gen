import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv



def Mail(receiver, subject, message):
    load_dotenv()
    API_KEY = os.getenv("key")
    SECRET_KEY = os.getenv("PASSWORD")
    SENDER = os.getenv("EMAIL")

    url = "https://api.mailjet.com/v3.1/send"

    data = {
        "Messages": [
            {
                "From": {
                    "Email": SENDER,
                    "Name": "AI STORY GEN"
                },
                "To": [
                    {
                        "Email": receiver
                    }
                ],
                "Subject": subject,
                "TextPart": message
            }
        ]
    }

    response = requests.post(
        url,
        auth=HTTPBasicAuth(API_KEY, SECRET_KEY),
        json=data
    )

    print(response.status_code)
    print(response.text)

    return response.status_code == 200