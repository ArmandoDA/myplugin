import os
import logging
from dotenv import load_dotenv
from novaclient import client as nova_client
from novaclient.exceptions import ClientException, Unauthorized, EndpointNotFound
from myplugin.notifier import send_email

# Carica variabili da .env
load_dotenv()

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("myplugin")

class MyPlugin:
    def __init__(self):
        self.active = False
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")
        if not self.recipient_email:
            logger.error("Variabile RECIPIENT_EMAIL mancante nel file .env.")
            raise ValueError("RECIPIENT_EMAIL non definita.")
        logger.info("MyPlugin inizializzato. Email destinatario: %s", self.recipient_email)

        self.nova = nova_client.Client(
            "2.1",
            username=os.getenv("OS_USERNAME"),
            password=os.getenv("OS_PASSWORD"),
            project_name=os.getenv("OS_PROJECT_NAME"),
            auth_url=os.getenv("OS_AUTH_URL")
        )

    def get_openstack_info(self):
        try:
            servers = self.nova.servers.list()
            info = {s.name: s.status for s in servers}
            return info
        except Unauthorized:
            return "Errore: credenziali non valide."
        except EndpointNotFound:
            return "Errore: endpoint Keystone non raggiungibile."
        except ClientException as e:
            return f"Errore client: {str(e)}"
        except Exception as e:
            return f"Errore generico: {str(e)}"

    def create_half_flavor(self, base_flavor):
        half_ram = int(base_flavor.ram / 2)
        half_vcpus = int(base_flavor.vcpus / 2)
        half_disk = int(base_flavor.disk / 2)
        flavor_name = f"half-{base_flavor.name}"

        for flavor in self.nova.flavors.list():
            if flavor.ram == half_ram and flavor.vcpus == half_vcpus and flavor.disk == half_disk:
                return flavor

        new_flavor = self.nova.flavors.create(
            name=flavor_name,
            ram=half_ram,
            vcpus=half_vcpus,
            disk=half_disk,
            id=None
        )
        logger.info("Creato nuovo flavor: %s", flavor_name)
        return new_flavor

    def resize_vm_to_half(self, vm_name):
        try:
            server = self.nova.servers.find(name=vm_name)
            current_flavor = self.nova.flavors.get(server.flavor['id'])
            target_flavor = self.create_half_flavor(current_flavor)
            server.resize(target_flavor.id)
            logger.info("Resize avviato per VM '%s' verso flavor '%s'", vm_name, target_flavor.name)
            return f"Resize avviato per VM '{vm_name}'"
        except Exception as e:
            logger.error("Errore nel resize della VM '%s': %s", vm_name, e)
            return f"Errore nel resize: {str(e)}"

    def confirm_vm_resize(self, vm_name):
        try:
            server = self.nova.servers.find(name=vm_name)
            server.confirm_resize()
            logger.info("Resize confermato per VM '%s'", vm_name)
            return f"Resize confermato per VM '{vm_name}'"
        except Exception as e:
            logger.error("Errore nella conferma del resize: %s", e)
            return f"Errore nella conferma: {str(e)}"

    def start(self):
        self.active = True
        logger.info("Plugin attivato.")
        try:
            send_email("Plugin Attivato", "Il plugin è ora attivo.", self.recipient_email)
        except Exception as e:
            logger.error("Errore nell'invio email di attivazione: %s", e)

        info = self.get_openstack_info()
        send_email("Parametri OpenStack", str(info), self.recipient_email)

        if isinstance(info, dict):
            for vm_name in info.keys():
                resize_result = self.resize_vm_to_half(vm_name)
                send_email(f"Resize VM {vm_name}", resize_result, self.recipient_email)
                confirm_result = self.confirm_vm_resize(vm_name)
                send_email(f"Conferma Resize VM {vm_name}", confirm_result, self.recipient_email)

    def stop(self):
        self.active = False
        logger.info("Plugin disattivato.")
        try:
            send_email("Plugin Disattivato", "Il plugin è stato disattivato.", self.recipient_email)
        except Exception as e:
            logger.error("Errore nell'invio email di disattivazione: %s", e)

    def execute(self, context=None):
        logger.info("Esecuzione del plugin con contesto: %s", context)
        if not self.active:
            logger.warning("Il plugin non è attivo. Attivazione automatica.")
            try:
                self.start()
            except Exception as e:
                logger.error("Errore durante l'attivazione automatica: %s", e)
                return "Errore durante l'esecuzione del plugin"

        try:
            result = "Esecuzione completata con successo"
            logger.info("Risultato: %s", result)
            return result
        except Exception as e:
            logger.error("Errore durante l'esecuzione: %s", e)
            return "Errore durante l'esecuzione del plugin"