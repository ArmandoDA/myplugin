#!/bin/bash

# Path del plugin
MYPLUGIN_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

function install_myplugin {
    echo "[myplugin] Installing myplugin..."
    # Installa le dipendenze Python se presenti
    if [[ -f "$MYPLUGIN_DIR/requirements.txt" ]]; then
        pip install -r "$MYPLUGIN_DIR/requirements.txt"
    fi
}

function configure_myplugin {
    echo "[myplugin] Configuring myplugin..."
    # Aggiungi qui eventuali configurazioni
}

function init_myplugin {
    echo "[myplugin] Initializing myplugin..."
    # Avvia eventuali servizi o esegui codice di inizializzazione
    # python3 $MYPLUGIN_DIR/main.py
}

# Hook DevStack
if [[ "$1" == "stack" && "$2" == "install" ]]; then
    install_myplugin
elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
    configure_myplugin
elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
    init_myplugin
fi
