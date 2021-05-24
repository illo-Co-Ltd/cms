import os
import cv2

ds_factor = 1


class VideoCamera:
    """
    Camera preprocess codes
    """

    def __init__(self, device_ip):
        self.url_stream = f'rtsp://{device_ip}/stream1'
        # self.url_jpeg =
        try:
            self.video = cv2.VideoCapture(self.url_stream)
        except:
            raise ConnectionError(f'Cannot connect to {self.url_stream}')

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
            self.video = cv2.VideoCapture(self.url_stream)
        except:
            raise Exception(f'Cannot reinitialize')
