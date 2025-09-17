import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, to_email):
    """
    Invia un'email usando il server SMTP di Gmail.
    """
    from_email = ""
    password = ""

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
