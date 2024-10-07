# Video_editor_ai.dp
WORK IN PROGRESS WILL INTEGRATE VIDEO GENERATION AI IN TIME AND MAKE THIS A FULL VIDEO EDITING TOOL FOR FREE USE

Here’s a draft README for your project, based on the files you provided:

---

# Video Processing Application

## Overview

This project is a video editing and processing web application that enables users to upload, edit, and manipulate video files directly from a web interface. It integrates various media transformation tasks using FFmpeg through a Flask-based backend and Celery for asynchronous task processing.

## Key Features

- **Video Uploading**: Users can upload video files through an intuitive frontend interface built with Bulma and Three.js for real-time interactions.
- **Video Editing**: The app supports several common video editing actions such as resizing, rotating, and converting to grayscale.
- **Asynchronous Processing**: Media processing tasks are managed asynchronously using Celery, allowing for efficient handling of larger files and operations without blocking the user interface.
- **Dark Mode**: A toggle option for dark mode to improve user experience.
- **3D Media Container**: The application provides a responsive 3D container for rendering and displaying media content interactively.

## Backend

The backend is built using Flask and integrates the following technologies:
- **FFmpeg**: Handles video processing such as resizing, rotating, and applying filters. The FFmpeg commands are executed via a Python subprocess wrapper.
- **Celery**: Manages the task queue for asynchronous media processing. It uses Redis as the message broker and backend for task result storage.
- **Flask**: Provides the API and web server to handle media upload, editing requests, and deliver processed videos back to the frontend.
  
## Frontend

The frontend is built using HTML, Bulma CSS, and JavaScript. Key frontend features include:
- A responsive interface for uploading and editing media.
- Real-time video preview and 3D interactive media container using Three.js.
- Video editing options that allow the user to select and apply transformations (resize, rotate, grayscale).

## How It Works

1. **Upload Video**: Users can upload video files (MP4, AVI, MOV, MKV) via the upload form.
2. **Select Editing Action**: Choose from resizing, rotating, or applying a filter like grayscale.
3. **Asynchronous Processing**: The processing tasks are handled by Celery, allowing the frontend to remain responsive while heavy video processing occurs in the background.
4. **Result Delivery**: Once the video is processed, the user is provided with a download link for the edited media.

## How to Run

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Redis
- FFmpeg

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/videoprocessing-app.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Redis:
   ```bash
   redis-server
   ```
4. Start the Celery worker:
   ```bash
   celery -A celeryworker.celery worker --loglevel=info
   ```
5. Start the Flask server:
   ```bash
   python vid.app.py
   ```

### Environment Variables

Create a `.env` file in the root directory with the following variables:
```
UPLOAD_FOLDER=frontend/static/uploads
EDITED_FOLDER=frontend/static/edited
```

### Running the Application

After following the setup steps, you can access the application at `http://localhost:5000` in your browser.

## Contributing

Feel free to fork the repository and submit pull requests. Contributions are welcome!
