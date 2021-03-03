import os
import cv2

ds_factor = 1
DEVICE_IP = os.getenv('DEVICE_IP')


class VideoCamera:
    """
    Camera preprocess codes
    """

    def __init__(self):
        self.url = f'rtsp://{DEVICE_IP}/stream1'
        try:
            self.video = cv2.VideoCapture(self.url)
        except:
            raise ConnectionError(f'Cannot connect to {self.url}')

    def __del__(self):
        # releasing camera
        self.video.release()

    def get_frame(self):
        # extracting frames
        ret, frame = self.video.read()
        if ret:
            return frame
        else:
            raise ValueError('Video read failed')

    def reinitialize(self):
        self.video.release()
        try:
            self.video = cv2.VideoCapture(self.url)
        except:
            raise Exception(f'Cannot reinitialize')
