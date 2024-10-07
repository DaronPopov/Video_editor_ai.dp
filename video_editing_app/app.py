import os
import uuid
import logging
import sys
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from werkzeug.utils import secure_filename
from celery_worker import process_media_task  # Import your Celery worker task

# Add the parent directory to sys.path to resolve module imports correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create Flask app and reference the correct directories for templates and static files
app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
CORS(app)

# Configure Logging
log_file = 'app.log'
with open(log_file, 'w'):  # Clear the existing log file content and create a new one
    pass
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv(find_dotenv())

# Configuration
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'frontend/static/uploads')
EDITED_FOLDER = os.getenv('EDITED_FOLDER', 'frontend/static/edited')

# Ensure upload and edited directories exist
upload_path = os.path.abspath(os.path.join(app.root_path, UPLOAD_FOLDER))
edited_path = os.path.abspath(os.path.join(app.root_path, EDITED_FOLDER))
os.makedirs(upload_path, exist_ok=True)
os.makedirs(edited_path, exist_ok=True)

# Allowed file extensions
def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'mkv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# Determine the media type based on file extension
def get_media_type(filename):
    video_extensions = {'mp4', 'avi', 'mov', 'mkv'}
    image_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in video_extensions:
        return 'video'
    elif ext in image_extensions:
        return 'image'
    else:
        return 'unknown'

# Route to serve the main index.html
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Route for uploading media files
@app.route('/upload', methods=['POST'])
def upload_media():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        media_type = get_media_type(filename)
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        return jsonify({'status': 'success', 'filename': filename, 'media_type': media_type})
    else:
        return jsonify({'error': 'Invalid file type'}), 400

# Route for applying video editing actions
@app.route('/edit', methods=['POST'])
def edit_media():
    data = request.json
    action = data.get('action')
    filename = data.get('filename')
    params = data.get('params', {})

    if not filename or not action:
        return jsonify({'error': 'Filename and action are required'}), 400

    input_path = os.path.join(upload_path, filename)
    output_filename = f"edited_{uuid.uuid4().hex}_{filename}"
    output_path = os.path.join(edited_path, output_filename)

    # Send the task to Celery worker
    task = process_media_task.apply_async(args=[input_path, output_path, action, params])

    return jsonify({'status': 'processing', 'task_id': task.id})

# Route to check task status
@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = process_media_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        return jsonify({'status': 'pending'}), 200
    elif task.state == 'SUCCESS':
        return jsonify({'status': 'success', 'output_path': task.result['output_path']}), 200
    elif task.state == 'FAILURE':
        return jsonify({'status': 'failed', 'error': str(task.info)}), 400
    else:
        return jsonify({'status': task.state}), 200

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
