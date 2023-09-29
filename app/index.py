from flask import Flask
from app.routers.mainRouters import mainRouters
from app.config.database import DatabaseBuilder

def createApp():
    # Config of app and Database
    app = Flask(__name__)
    auxDB = DatabaseBuilder().build()

    # Routes of app
    mainRouters(app=app, auxDB=auxDB)

    return app