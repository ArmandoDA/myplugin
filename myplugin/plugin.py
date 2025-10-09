# In questo file vengono invocati i due metodi utili al funzionamento
# del plugin e vengono definite le fasi di start, stop ed execute

import os
import logging
from dotenv import load_dotenv
from myplugin.notifier import send_email
from myplugin.openstack_info import get_openstack_info

# Carica variabili da .env
load_dotenv()

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("myplugin")

class MyPlugin:
    def __init__(self):
        self.active = False
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")
        logger.info("MyPlugin inizializzato. Email destinatario: %s", self.recipient_email)

    def start(self):
        self.active = True
        logger.info("Plugin attivato.")
        send_email("Plugin Attivato", "Il plugin è ora attivo.", self.recipient_email)
        info = get_openstack_info()
        logger.info("Informazioni OpenStack ottenute: %s", info)
        send_email("Parametri OpenStack", info, self.recipient_email)

    def stop(self):
        self.active = False
        logger.info("Plugin disattivato.")
        send_email("Plugin Disattivato", "Il plugin è stato disattivato.", self.recipient_email)

    def execute(self, context=None):
        logger.info("Esecuzione del plugin con contesto: %s", context)
        if not self.active:
            logger.warning("Il plugin non è attivo. Attivazione automatica.")
            self.start()
        result = "Esecuzione completata con successo"
        logger.info("Risultato: %s", result)
        return result