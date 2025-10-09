# MyPlugin - OpenStack Automation Plugin

## 📌 Descrizione

**MyPlugin** è un plugin Python che automatizza operazioni su macchine virtuali OpenStack. Utilizza `python-novaclient` per interagire con l'infrastruttura e invia notifiche via email. Le funzionalità principali includono:

- Recupero dello stato delle VM
- Invio email con informazioni sulle VM
- Ridimensionamento automatico delle VM verso flavor con metà risorse
- Creazione di flavor personalizzati se necessario
- Conferma automatica del resize

---

## ⚙️ Requisiti software

- Python 3.7+
- OpenStack con Keystone v3
- Permessi per accedere alle VM e creare flavor
- Accesso SMTP per invio email (gestito dal modulo `notifier`)
- File `.env` con variabili di configurazione

---

# INSTALLAZIONE MACCHINA VIRTUALE

    -Requisiti di sistema
        Hypervisor: VirtualBox (utilizzato) / VMware / KVM
        ISO: Ubuntu Server 22.04 LTS (consigliato)
    -Risorse consigliate:
        CPU: 4 core
        RAM: 8 GB
        Disco: 50 GB

    -Creare una nuova VM con Ubuntu Server.
    -Impostare la rete in modalità "Bridged" o "NAT con port forwarding".
    -Installare Ubuntu e aggiornare il sistema con il comando:
        sudo apt update && sudo apt upgrade -y

    -Creare un utente non root (stack) con i comandi: 
        sudo useradd -s /bin/bash -d /opt/stack -m stack
        echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack


# INSTALLAZIONE OPENSTACK

    -Clonare repository Devstack con i comandi:
        sudo su - stack
        git clone https://opendev.org/openstack/devstack
        cd devstack

    -Creare file local.conf con il comando:    
        nano local.conf

    -Inserire il contenuto di default:
        [[local|localrc]]
        ADMIN_PASSWORD=secret
        DATABASE_PASSWORD=$ADMIN_PASSWORD
        RABBIT_PASSWORD=$ADMIN_PASSWORD
        SERVICE_PASSWORD=$ADMIN_PASSWORD

    -Avviare l'installazione con il comando:
        ./stack.sh

    -In caso di errori durante l'installazione, eseguire i seguenti comandi:
        ./unstack.sh (disinstallare l'ambiente)
        ./clean.sh (rimuovere tutti i file installati)
        ./stack.sh (riavviare l'installazione)


# INSTALLAZIONE PLUGIN PERSONALIZZATO

    -Modificare il file local.conf aggiungendo la stringa:
        enable_plugin myplugin https://github.com/ArmandoDA/myplugin
    -disinstallare e installare di nuovo l'ambiente con i comandi:
        ./unstack.sh (disinstallare l'ambiente)
        ./clean.sh (rimuovere tutti i file installati)
        ./stack.sh (riavviare l'installazione)


# VERIFICA DELL'INSTALLAZIONE

    -Eseguire uno di questi comandi:     
        source openrc
        openstack service list
        openstack endpoint list
    -Oppure accedere al dashboard Horizon via browser:
        http://<IP_VM>:80 
    -Se non si conosce l'indirizzo della VM (dovrebbe essere 192.168.1.168) utilizzare il comando:    
        hostname -I
