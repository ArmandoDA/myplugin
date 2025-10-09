# In questo file viene gestita la logica per 
# recuperare informazioni base da OpenStack (es. istanze attive)

from novaclient import client as nova_client
from novaclient.exceptions import ClientException, Unauthorized, EndpointNotFound
import os
from dotenv import load_dotenv

load_dotenv()  # Carica le variabili dal file .env

def get_openstack_info():

    try:
        nova = nova_client.Client(
            "2.1",
            username=os.getenv("OS_USERNAME"),
            password=os.getenv("OS_PASSWORD"),
            project_name=os.getenv("OS_PROJECT_NAME"),
            auth_url=os.getenv("OS_AUTH_URL")
        )

        servers = nova.servers.list()
        info = "\n".join([f"Istanza: {s.name}, Stato: {s.status}" for s in servers])
        return info

    except Unauthorized:
        return "Errore: credenziali non valide per OpenStack."

    except EndpointNotFound:
        return "Errore: endpoint Keystone non raggiungibile."

    except ClientException as e:
        return f"Errore client OpenStack: {str(e)}"

    except Exception as e:
        return f"Errore generico: {str(e)}"
