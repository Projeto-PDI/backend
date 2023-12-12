from flask import request, redirect, jsonify, render_template
from app.services.TrajectoryVelocityProcessing import (
    TrajectoryVelocityProcessing,
    HelmetProcessing,
)
import io

trajectories_processing = TrajectoryVelocityProcessing()
helmet_processing = HelmetProcessing()


def mainRouters(app, auxDB):
    @app.route("/", methods=["GET"])
    def home():
        return render_template("index.html")

    @app.route("/docs", methods=["GET"])
    def default():
        redirect("/swagger")

    @app.route("/register", methods=["POST"])
    def upload():
        try:
            name = request.form["name"]
            file = request.files["file"]

            file_copy_1 = io.BytesIO(file.read())
            file_copy_2 = io.BytesIO(file.read())

            traj_data = trajectories_processing.process(file_copy_1)
            helmet_data = helmet_processing.process(file_copy_2)

            registro_token = auxDB.create_trajectories(traj_data, name)
            auxDB.create_helmet(helmet_data, registro_token)

            return jsonify(registro_token)
        except Exception as e:
            return jsonify(
                {"message": f"Error: {e}, me ajuda por favor: {helmet_data}!"}
            )

    @app.route("/register/<name>", methods=["GET"])
    def get(name):
        try:
            data = auxDB.get_register(name)

            return jsonify(data)
        except Exception as e:
            return jsonify({"message": f"Error: {e}!"})
