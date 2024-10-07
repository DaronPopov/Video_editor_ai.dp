from lumaai import LumaAI
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class LumaAI:
    def __init__(self, api_key):
        self.client = LumaAI(api_key=api_key)

    def generate_video(self, text_prompt, keyframes=None, looping=False, aspect_ratio='16:9'):
        """
        Generates a video based on the given text prompt.

        :param text_prompt: The input prompt for video generation.
        :param keyframes: Optional keyframe settings for more control.
        :param looping: Whether the video should loop.
        :param aspect_ratio: Aspect ratio for the video.
        :return: Video URL once generation is complete.
        """
        request = self.client.generations.create(
            prompt=text_prompt,
            keyframes=keyframes,
            looping=looping,
            aspect_ratio=aspect_ratio
        )
        return self._poll_for_result(request)

    def _poll_for_result(self, request):
        """
        Polls for the result of a video generation request.

        :param request: The video generation request to poll for.
        :return: The URL of the generated video.
        """
        while not request.status == 'complete':
            time.sleep(5)
            request.update_status()
        if request.status == 'complete' and request.success:
            return request.result_url
        else:
            raise Exception(f"Video generation failed: {request.error_message}")

    def extend_video(self, video_url, text_prompt, new_length):
        """
        Extends an existing video using a new text prompt.

        :param video_url: URL of the existing video to extend.
        :param text_prompt: The input prompt for extension.
        :param new_length: Desired length of the extended video.
        :return: Extended video URL once complete.
        """
        request = self.client.generations.extend(
            video_url=video_url,
            prompt=text_prompt,
            length=new_length
        )
        return self._poll_for_result(request)

    def interpolate_videos(self, video_url_1, video_url_2):
        """
        Creates an interpolation between two given videos.

        :param video_url_1: URL of the first video.
        :param video_url_2: URL of the second video.
        :return: Interpolated video URL.
        """
        request = self.client.generations.interpolate(
            video_1=video_url_1,
            video_2=video_url_2
        )
        return self._poll_for_result(request)

    def generate_video_via_api(self, text_prompt, keyframes=None, looping=False, aspect_ratio='16:9'):
        """
        Generates a video via API call for integration into software.

        :param text_prompt: The input prompt for video generation.
        :param keyframes: Optional keyframe settings for more control.
        :param looping: Whether the video should loop.
        :param aspect_ratio: Aspect ratio for the video.
        :return: Video URL once generation is complete.
        """
        video_url = self.generate_video(text_prompt, keyframes, looping, aspect_ratio)
        # Sending the generated video URL back to the main UI for rendering
        self.send_to_ui(video_url)
        return video_url

    def send_to_ui(self, video_url):
        """
        Sends the generated video URL to the main UI for rendering in the frontend.

        :param video_url: The URL of the generated video.
        """
        # Implementation to communicate with the main UI
        # This could be a REST API call, WebSocket message, or any other form of communication
        print(f"Video URL sent to UI: {video_url}")

# Example usage
# luma = LumaAI(api_key=os.getenv("LUMA_API_KEY"))
# video_url = luma.generate_video_via_api("A serene beach at sunset")
# print(video_url)