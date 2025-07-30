
from novaclient import client as nova_client
from novaclient.exceptions import ClientException, Unauthorized, EndpointNotFound

def get_openstack_info():
    """
    Recupera informazioni base da OpenStack (es. istanze attive).
    Gestisce errori di connessione, autenticazione e API.
    """
    try:
        nova = nova_client.Client(
            "2.1",
            username="admin",
            password="nomoresecret",
            project_name="admin",
            auth_url="http://192.168.1.168/identity"
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