from flask import Flask, request, send_from_directory
from flask_restful import Api, Resource
import os

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class FileResource(Resource):
    def post(self):
        if 'file' not in request.files:
            return 'No file part', 400

        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return 'File uploaded successfully', 200

    def get(self, filename=None):
        if filename:
            try:
                return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
            except FileNotFoundError:
                return 'File not found', 404
        else:
            files = os.listdir(app.config['UPLOAD_FOLDER'])
            return files, 200

    def delete(self, filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return 'File deleted successfully', 200
        else:
            return 'File not found', 404

api.add_resource(FileResource, '/files', '/files/<string:filename>')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
