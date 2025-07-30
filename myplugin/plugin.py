from myplugin.notifier import send_email
from myplugin.openstack_info import get_openstack_info

class MyPlugin:
    def __init__(self):
        self.active = False

    def start(self):
        """
        Attiva il plugin e invia email di notifica.
        """
        self.active = True
        send_email("Plugin Attivato", "Il plugin è ora attivo.", "a.dangelo65@studenti.unisa.it")

        # Invia anche parametri da OpenStack
        info = get_openstack_info()
        send_email("Parametri OpenStack", info, "a.dangelo65@studenti.unisa.it")

    def stop(self):
        """
        Disattiva il plugin e invia email di notifica.
        """
        self.active = False
        send_email("Plugin Disattivato", "Il plugin è stato disattivato.", "a.dangelo65@studenti.unisa.it")
