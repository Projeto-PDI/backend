from flask import request, redirect, render_template, jsonify
from app.services.TrajectoryVelocityProcessing import TrajectoryVelocityProcessing

data_processing = TrajectoryVelocityProcessing()

def mainRouters(app, auxDB):
    @app.route('/', methods=['GET'])
    def default():
        redirect('/swagger')
    
    @app.route('/home', methods=['GET'])
    def home():
        return render_template('index.html')
    
    @app.route('/upload', methods=['POST'])
    def upload():
        if request.method == 'POST':
            file = request.files['file']

            data = data_processing.process(file)

            return jsonify(data)
    
    @app.route('/data', methods=['GET'])
    def testBD():
        return jsonify(auxDB.get_all_register())
    
    @app.route('/createData', methods=['GET'])
    def createData():
        try:
            auxDB.create_register()
            return jsonify({"message": "Data created with success!"})
        except Exception as e:
            return jsonify({"message": f"Error: {e}!"})