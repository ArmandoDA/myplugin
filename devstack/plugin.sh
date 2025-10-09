#!/bin/bash

PLUGIN_DIR=$DEST/myplugin
PLUGIN_MAIN=$PLUGIN_DIR/myplugin.py
PLUGIN_LOG=$DEST/logs/myplugin.log
PLUGIN_ENV=$PLUGIN_DIR/.env

function install_myplugin {
    echo "Installing myplugin..."
    # Clona il repository se non già presente
    if [ ! -d "$PLUGIN_DIR" ]; then
        git clone https://github.com/ArmandoDA/myplugin.git $PLUGIN_DIR
    fi

    # Installa le dipendenze Python
    pip install -r $PLUGIN_DIR/requirements.txt
}

function configure_myplugin {
    echo "Configuring myplugin..."
    # Assicura che il file .env esista
    if [ ! -f "$PLUGIN_ENV" ]; then
        echo "RECIPIENT_EMAIL=admin@example.com" > $PLUGIN_ENV
        echo "Creato file .env con email di default"
    fi
}

function start_myplugin {
    echo "Starting myplugin..."
    # Avvia il plugin in background e salva log
    nohup python3 $PLUGIN_MAIN > $PLUGIN_LOG 2>&1 &
    echo $! > $DEST/myplugin.pid
    echo "Plugin avviato con PID $(cat $DEST/myplugin.pid)"
}

function stop_myplugin {
    echo "Stopping myplugin..."
    if [ -f "$DEST/myplugin.pid" ]; then
        kill $(cat $DEST/myplugin.pid) && rm $DEST/myplugin.pid
        echo "Plugin fermato."
    else
        echo "PID file non trovato. Plugin potrebbe non essere attivo."
    fi
}

if [[ "$1" == "stack" ]]; then
    case "$2" in
        install)
            install_myplugin
            ;;
        post-config)
            configure_myplugin
            ;;
        extra)
            start_myplugin
            ;;
    esac
elif [[ "$1" == "unstack" ]]; then
    stop_myplugin
elif [[ "$1" == "clean" ]]; then
    echo "Cleaning myplugin..."
    rm -rf $PLUGIN_DIR
    rm -f $DEST/myplugin.pid
    rm -f $PLUGIN_LOG
fi
