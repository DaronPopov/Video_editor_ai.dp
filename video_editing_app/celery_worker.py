from celery import Celery
import os
import subprocess
import logging
from celery.exceptions import SoftTimeLimitExceeded

# Import the FFmpegProcessor from the correct module
from modules.ffmpeg_module import FFmpegProcessor

# Configure logging
log_file = 'celery.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a Celery app
def make_celery(app_name=__name__):
    return Celery(app_name, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

celery = make_celery()

@celery.task(bind=True, soft_time_limit=300, max_retries=3)
def process_media_task(self, input_path, output_path, action, params):
    processor = FFmpegProcessor(input_file=input_path, output_file=output_path)
    try:
        if action == 'resize_video':
            width = params.get('width')
            height = params.get('height')
            if width is None or height is None:
                raise ValueError("Width and height parameters are required for resizing.")
            processor.resize_video(width, height)

        elif action == 'rotate_video':
            degrees = params.get('degrees')
            if degrees is None:
                raise ValueError("Degrees parameter is required for rotation.")
            processor.rotate_video(int(degrees))

        elif action == 'convert_to_grayscale':
            processor.convert_to_grayscale()

        elif action == 'crop_video':
            width = params.get('width')
            height = params.get('height')
            x = params.get('x', 0)
            y = params.get('y', 0)
            if width is None or height is None:
                raise ValueError("Width and height are required for cropping.")
            processor.crop_video(width, height, x, y)

        elif action == 'extract_audio':
            processor.extract_audio()

        else:
            raise ValueError(f"Unsupported action: {action}")

        # Log success and return the output path
        logging.info(f"Task {self.request.id} completed successfully: {output_path}")
        return {'status': 'success', 'output_path': output_path}

    except SoftTimeLimitExceeded:
        # Retry the task if time limit is exceeded
        logging.error(f"Task {self.request.id} timed out.")
        self.retry(countdown=60, max_retries=3)

    except Exception as e:
        # Log the error and update the Celery task state to FAILURE
        logging.error(f"Task {self.request.id} failed: {e}")
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise

# This module uses Celery for asynchronous task management
