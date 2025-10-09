# In questo file viene gestita la logica per inviare una mail

import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()  # Carica le variabili dal file .env

def send_email(subject, body, to_email):
    from_email = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.sendmail(from_email, [to_email], msg.as_string())
        print("Email inviata con successo.")
    except Exception as e:
        print(f"Errore nell'invio dell'email: {e}")
