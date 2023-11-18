from flask import request, redirect, render_template, jsonify
from app.services.processFile import ProcessFile

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
            file.save(file.filename)

            data = ProcessFile().getInfo(file=file)

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