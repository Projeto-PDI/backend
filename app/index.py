from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from app.routers.mainRouters import mainRouters
from app.routers.swaggerRoutes import swwagerRoutes
from app.config.database import DatabaseBuilder

def createApp():
    # Config of app and Database
    app = Flask(__name__)
    auxDB = DatabaseBuilder().build()

    # Configure Swagger UI
    SWAGGER_URL = '/swagger'
    API_URL = 'http://localhost:5000/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Sample API"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Routes of app
    mainRouters(app=app, auxDB=auxDB)
    swwagerRoutes(app=app,auxDB=auxDB)

    return app