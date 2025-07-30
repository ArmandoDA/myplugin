
#!/bin/bash

# Path del plugin
MYPLUGIN_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

function install_myplugin {
    echo "[myplugin] Installing myplugin..."
    if [[ -f "$MYPLUGIN_DIR/requirements.txt" ]]; then
        pip install -r "$MYPLUGIN_DIR/requirements.txt"
    fi
}

function configure_myplugin {
    echo "[myplugin] Configuring myplugin..."
    # Eventuali configurazioni
}

function init_myplugin {
    echo "[myplugin] Initializing myplugin..."
    # Avvia il servizio come processo DevStack
    run_process myplugin "python3 $MYPLUGIN_DIR/myplugin/service.py"
}

function stop_myplugin {
    echo "[myplugin] Stopping myplugin..."
    stop_process myplugin
}

# Hook DevStack
if [[ "$1" == "stack" && "$2" == "install" ]]; then
    install_myplugin
elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
    configure_myplugin
elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
    init_myplugin
elif [[ "$1" == "unstack" ]]; then
    stop_myplugin
fi
