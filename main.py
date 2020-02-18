from flask_restful import Api

from apps import create_app
from resources import (Register, Login, Search, Insert, Update)
from source.configuration import application_config

# Create flask application
application = create_app(application_config)
# Make an restful API
api = Api(application)
# Add register endpoint
api.add_resource(Register, "/register")
# Add login endpoint
api.add_resource(Login, "/login")
# Add searching endpoint
api.add_resource(Search, "/search")
# Add insertion endpoint
api.add_resource(Insert, "/insert")
# Add update endpoint
api.add_resource(Update, "/update")

if __name__ == '__main__':
    application.run("0.0.0.0", port=8080)
