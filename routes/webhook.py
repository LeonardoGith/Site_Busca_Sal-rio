from flask import Blueprint, request, abort

import subprocess
import os

webhook_route = Blueprint('webhook', __name__)

# The path to your web app directory
WORK_DIR = '/home/LeonardoSv/buscasalario'

@webhook_route.route('/', methods=['POST'])
def git_pull():
    if request.method == 'POST':
        # You can add a check here for a specific secret to ensure it's from GitHub
        subprocess.run(["python3", os.path.join(WORK_DIR, "git_pull.py")])
        return "Pulling latest changes from GitHub...", 200
    else:
        abort(400)

@webhook_route.route('', methods=['POST'])
def git_pull_root():
    if request.method == 'POST':
        # You can add a check here for a specific secret to ensure it's from GitHub
        subprocess.run(["python3", os.path.join(WORK_DIR, "git_pull.py")])
        return "Pulling latest changes from GitHub...", 200
    else:
        abort(400)
