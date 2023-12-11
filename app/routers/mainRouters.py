from flask import request, redirect, jsonify
from app.services.TrajectoryVelocityProcessing import TrajectoryVelocityProcessing

data_processing = TrajectoryVelocityProcessing()


def mainRouters(app, auxDB):
    @app.route("/docs", methods=["GET"])
    def default():
        redirect("/swagger")

    @app.route("/file_upload", methods=["POST"])
    def upload():
        try:
            file = request.files["file"]

            data = data_processing.process(file)

            return jsonify(data)
        except Exception as e:
            return jsonify({"message": f"Error: {e}!"})
