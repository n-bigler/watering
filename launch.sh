#!/bin/sh

tmux new-session -d -s watering 
tmux rename-window 'editor'
tmux new-window 
tmux rename-window 'services'
tmux send-keys 'cd db && source venv-db/bin/activate && python dbmanager.py' Enter
sleep 1
tmux split-window -h 
tmux send-keys 'cd gpio && source venv-gpio/bin/activate && python gpioManager.py' Enter
tmux split-window -v 
tmux send-keys 'cd devices && source venv-device/bin/activate && python deviceManager.py' Enter
tmux split-window -h 
tmux send-keys 'cd logger && source venv-logger/bin/activate && python logger.py' Enter
tmux split-window -h 
tmux send-keys 'cd process && source venv-process/bin/activate && python processManager.py' Enter
tmux select-layout tiled
tmux new-window 
tmux rename-window 'web'
tmux send-keys 'cd web && source venv-web/bin/activate && python app.py' Enter
tmux split-window -h 
tmux send-keys 'cd web && npm run start' Enter
tmux -2 attach-session -t watering
