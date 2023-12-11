from flask import request, redirect, jsonify
from app.services.processFile import ProcessFile


def mainRouters(app, auxDB):
    @app.route("/docs", methods=["GET"])
    def default():
        redirect("/swagger")

    @app.route("/file_upload", methods=["POST"])
    def upload():
        try:
            file = request.files["file"]
            file.save(file.filename)

            data = ProcessFile().getInfo(file=file)

            return jsonify(data)
        except Exception as e:
            return jsonify({"message": f"Error: {e}!"})
