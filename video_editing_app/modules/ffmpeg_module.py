import subprocess
import logging

class FFmpegProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def resize_video(self, width, height):
        command = f"ffmpeg -i {self.input_file} -vf scale={width}:{height} {self.output_file}"
        self._run_command(command)

    def rotate_video(self, degrees):
        command = f"ffmpeg -i {self.input_file} -vf 'rotate={degrees}*PI/180' {self.output_file}"
        self._run_command(command)

    def convert_to_grayscale(self):
        command = f"ffmpeg -i {self.input_file} -vf format=gray {self.output_file}"
        self._run_command(command)

    def crop_video(self, width, height, x=0, y=0):
        command = f"ffmpeg -i {self.input_file} -filter:v 'crop={width}:{height}:{x}:{y}' {self.output_file}"
        self._run_command(command)

    def extract_audio(self):
        command = f"ffmpeg -i {self.input_file} -q:a 0 -map a {self.output_file}.mp3"
        self._run_command(command)

    def _run_command(self, command):
        try:
            logging.info(f"Running command: {command}")
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"FFmpeg command failed: {e}")
            raise
