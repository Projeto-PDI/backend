from flask import request, redirect, jsonify, render_template, url_for
from app.services.TrajectoryVelocityProcessing import (
    TrajectoryVelocityProcessing,
    HelmetProcessing,
)
from werkzeug.datastructures import FileStorage
from io import BytesIO

trajectories_processing = TrajectoryVelocityProcessing()
helmet_processing = HelmetProcessing()




def mainRouters(app, auxDB):
    @app.route("/", methods=["GET"])
    def home():
        return redirect("/swagger")

    @app.route("/register", methods=["POST"])
    def createRegister():
        try:
            name = request.form["name"]
            file = request.files["file"]
                
            traj_data = trajectories_processing.process(file)
            
            # Cópia do arquivo para segundo processamento
            file.stream.seek(0)
            file_bytes = file.stream.read()
            file_copy = FileStorage(
                stream=BytesIO(file_bytes),
                filename=file.filename,
                content_type=file.content_type,
            )
            
            helmet_data = helmet_processing.process(file_copy)
            
            registro_token = auxDB.create_trajectories(traj_data, name)
            auxDB.create_helmet(helmet_data, registro_token)

            return jsonify(registro_token)
        except Exception as e:
            return jsonify(
                {"message": f"Error: {e}!"}
            )

    @app.route("/register/", methods=["GET"])
    def getAllRegister():
        try:
            data = auxDB.get_all_registers()

            return jsonify(data)
        except Exception as e:
            return jsonify({"message": f"Error: {e}!"})

    @app.route("/register/<id>", methods=["GET"])
    def getRegister(id):
        try:
            data = auxDB.get_registro_by_token(id)

            return jsonify(data)
        except Exception as e:
            return jsonify({"message": f"Error: {e}!"})
