from flask import request, redirect, jsonify, render_template
from app.services.TrajectoryVelocityProcessing import TrajectoryVelocityProcessing

data_processing = TrajectoryVelocityProcessing()


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

            data = data_processing.process(file)
            auxDB.create_trajectories(data, name)

            return jsonify(data)
        except Exception as e:
            return jsonify({"message": f"Error: {e}!"})

    @app.route("/register/<name>", methods=["GET"])
    def get(name):
        try:
            data = auxDB.get_register(name)

            return jsonify(data)
        except Exception as e:
            return jsonify({"message": f"Error: {e}!"})
