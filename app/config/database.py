import os
from pymongo import MongoClient

class DatabaseBuilder:
    def build(self):
        DB_NAME = os.getenv("MONGO_INITDB_DATABASE")
        COLLECTION_NAME = "trajectories"

        mongo = MongoClient(
            host="pdi_transport",
            port=27017,
            username=os.getenv("MONGO_INITDB_ROOT_USERNAME"),
            password=os.getenv("MONGO_INITDB_ROOT_PASSWORD"),
            authSource="admin"
        )

        client = mongo[DB_NAME]
        auxDB = client[COLLECTION_NAME]

        return auxDB