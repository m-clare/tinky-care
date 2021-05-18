source ~/.zshrc  
workon tinky-care
python3 ${HOME}/workspaces/current/tinky-care/bots/orgbot.py
scp ${HOME}/workspaces/current/tinky-care/assets/org.png pi@raspberrypi.local:~/projects/tinky-care/assets
deactivate
