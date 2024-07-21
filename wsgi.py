# Portfolio_Tracker/wsgi.py


import git
from flask import request
from app import app, create_app

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/PortfolioTracker/Portfolio_Tracker')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400
    
app = create_app()

